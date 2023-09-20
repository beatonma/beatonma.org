import React, { useState, useEffect, StrictMode, HTMLProps } from "react";
import { createRoot } from "react-dom/client";
import { animatedItemProps } from "../../page-transitions";
import { groupBy } from "../../util/array";
import { loadJson } from "../../util/requests";

const CONTAINER = "#webmentions";
const getContainerElement = () => document.getElementById("webmentions");
const DataAttr = { EmptyMessage: "data-empty-message" };

interface MentionsResponse {
    target_url: string;
    mentions: Mention[];
}
interface HCard {
    name: string;
    avatar?: string;
    homepage: string;
}
interface Mention {
    hcard: HCard;
    quote?: string;
    source_url: string;
    published: string;
    type: string;
}

export const WebmentionsApp = async (dom: Document | Element) => {
    const container = dom.querySelector(CONTAINER);

    if (container) {
        const root = createRoot(container);
        root.render(
            <StrictMode>
                <Webmentions />
            </StrictMode>
        );
    }
};

export const Webmentions = () => {
    const [mentions, setMentions] = useState(null);
    const [emptyMessage, setEmptyMessage] = useState<string>();

    useEffect(() => {
        const _emptyMessage = getContainerElement().getAttribute(
            DataAttr.EmptyMessage
        );
        if (_emptyMessage !== undefined) {
            setEmptyMessage(_emptyMessage);
        }
    }, []);

    useEffect(() => {
        const url = new URL(
            `${window.location.protocol}//${window.location.host}/webmention/get`
        );
        url.searchParams.append("url", window.location.pathname);

        loadJson<MentionsResponse>(url.href)
            .then(data => data.mentions)
            .then((mentions: Mention[]) => {
                const keys: string[] = [];
                const unique = mentions.filter(x => {
                    if (keys.includes(x.source_url)) return false;
                    else {
                        keys.push(x.source_url);
                        return true;
                    }
                });
                return unique;
            })
            .then(setMentions)
            .catch(console.error);
    }, []);

    if (mentions) {
        return (
            <MentionsContainer
                mentions={mentions}
                emptyMessage={emptyMessage}
            />
        );
    }
    return null;
};

interface MentionsContainerProps {
    mentions: Mention[];
    emptyMessage: string | undefined;
}
const MentionsContainer = (props: MentionsContainerProps) => {
    const { mentions, emptyMessage } = props;
    const isEmpty = mentions.length === 0;

    if (isEmpty && !emptyMessage) {
        return null;
    }

    return (
        <>
            <h3>Mentions</h3>
            <Mentions mentions={mentions} emptyMessage={emptyMessage} />
        </>
    );
};

interface MentionsProps {
    mentions: Mention[];
    emptyMessage: string;
}
const Mentions = (props: MentionsProps) => {
    const { mentions, emptyMessage } = props;

    if (mentions.length === 0)
        return <div className="mentions-empty">{emptyMessage}</div>;

    const { withQuotes, noQuotes } = groupBy(mentions, item =>
        item.quote ? "withQuotes" : "noQuotes"
    );

    return (
        <div className="grouped-mentions">
            <MentionsList mentions={withQuotes} data-quoted={true} />
            <MentionsList mentions={noQuotes} data-quoted={false} />
        </div>
    );
};

const MentionsList = (props: { mentions: Mention[] }) => {
    const { mentions, ...rest } = props;
    if (!mentions) return null;

    return (
        <div className="mentions" {...rest}>
            {mentions.map((m, index) => {
                const animationProps = animatedItemProps(index);
                return (
                    <Webmention
                        key={m.published}
                        mention={m}
                        {...animationProps}
                    />
                );
            })}
        </div>
    );
};

interface MentionProps {
    mention: Mention;
}
const Webmention = (props: MentionProps & HTMLProps<HTMLAnchorElement>) => {
    const { mention, className, title, href, ...rest } = props;
    const hasQuote = mention.quote != null;

    return (
        <a
            className="mention"
            title={mention.source_url}
            href={mention.source_url}
            data-quoted={hasQuote}
            {...rest}
        >
            <HCardInfo hcard={mention.hcard} sourceUrl={mention.source_url} />
            <Quote quote={mention.quote} />
        </a>
    );
};

interface HCardProps {
    hcard?: HCard;
    sourceUrl: string;
}
const HCardInfo = (props: HCardProps) => {
    const { hcard, sourceUrl } = props;

    const { name, avatar, homepage = sourceUrl } = hcard ?? {};
    const displayText = name ?? homepage.replace(/(https?:\/\/)?(www.)?/, "");

    return (
        <div className="mention-hcard">
            <Avatar name={name} avatar={avatar} homepage={homepage} />
            <div className="hcard-name">{displayText}</div>
        </div>
    );
};

const Avatar = (props: HCard) => {
    const { name, avatar, homepage } = props;

    if (!avatar) return <NullAvatar {...props} />;

    return (
        <img
            loading="lazy"
            src={avatar}
            className="mention-avatar"
            alt={name}
        />
    );
};

const NullAvatar = (props: HCard) => {
    const { name, homepage } = props;

    const homepageInitial = () => {
        try {
            return new URL(homepage).host.replace("www.", "")[0];
        } catch {
            return "?";
        }
    };

    const initial = name?.[0] ?? homepageInitial();
    return <div className="mention-avatar-null">{initial}</div>;
};

interface QuoteProps {
    quote?: string;
}
const Quote = (props: QuoteProps) => {
    const { quote } = props;
    if (!quote) return null;

    return <blockquote className="mention-quote">{quote}</blockquote>;
};
