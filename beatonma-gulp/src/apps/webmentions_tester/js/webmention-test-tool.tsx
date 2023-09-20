import React, {
    HTMLAttributes,
    KeyboardEvent,
    StrictMode,
    useEffect,
    useState,
} from "react";
import { createRoot } from "react-dom/client";
import { Dropdown } from "../../main/js/components/dropdown";
import { Row } from "../../main/js/components";
import { AppIcon, MaterialIcon } from "../../main/js/components/icons";
import { classes } from "../../main/js/components/props";
import { formatTimeDelta } from "../../main/js/util/datetime";
import { getCsrfToken } from "../../main/js/util/cookies";
import { loadJson } from "../../main/js/util/requests";
import { TitleBar } from "../../main/js/components/title-bar";

const ContainerSelector = "#webmentions_testing_tool";
const Endpoint = "active/";
const StatusPollingMillis = 3000;

interface TemporaryMentionsResponse {
    ttl: number;
    mentions: ActiveMention[];
}

interface MentionStatus {
    successful: boolean;
    status_code: number;
    message: string;
    source_url: string;
    target_url: string;
    endpoint: string;
}

interface ActiveMention {
    url: string;
    submitted_at: string | Date;
    expires_at: string | Date;
    expires_in: number;
    status: MentionStatus;
}

export const WebmentionTesterApp = async (dom: Document | Element) => {
    const container = dom.querySelector(ContainerSelector);

    if (container) {
        const root = createRoot(container);
        root.render(
            <StrictMode>
                <WebmentionsTester />
            </StrictMode>
        );
    }
};

const WebmentionsTester = () => {
    const [refreshFlag, setRefreshFlag] = useState(true);

    const refresh = () => setRefreshFlag(!refreshFlag);

    return (
        <>
            <CreateTempMention onSubmit={refresh} />
            <ActiveMentions onChange={refreshFlag} refresh={refresh} />
        </>
    );
};

interface ActiveMentionsProps {
    onChange: boolean;
    refresh: () => void;
}

const ActiveMentions = (props: ActiveMentionsProps) => {
    const [ttl, setTtl] = useState(0);
    const [mentions, setMentions] = useState([]);

    const { refresh, onChange } = props;

    useEffect(() => {
        loadJson<TemporaryMentionsResponse>(Endpoint).then(data => {
            setTtl(data.ttl);

            const mentions: ActiveMention[] = data.mentions;
            const uniqueUrlMentions = [
                ...new Map(mentions.map(item => [item.url, item])).values(),
            ];

            setMentions(uniqueUrlMentions);
        });
    }, [onChange]);

    const timeout = formatTimeDelta(ttl, {
        verbose: true,
    });
    const requestUpdate = (callback: () => void) => {
        setTimeout(() => {
            refresh();
            callback();
        }, StatusPollingMillis);
    };

    return (
        <section>
            <TitleBar
                title={<h2>Active mentions</h2>}
                labels={
                    <Label>{`Temporary mentions submitted in the last ${timeout}`}</Label>
                }
            />

            <div className="active-mentions">
                <SampleActiveMention
                    ttl={ttl}
                    expanded={mentions.length === 0}
                />
                {mentions.map(m => (
                    <ActiveMentionUI
                        mention={m}
                        key={m.submitted_at}
                        expanded={false}
                        requestUpdate={requestUpdate}
                    />
                ))}
            </div>
        </section>
    );
};

interface SampleActiveMentionProps {
    ttl: number;
    expanded: boolean;
}

const SampleActiveMention = (props: SampleActiveMentionProps) => {
    const submittedAt = new Date();
    const expiresAt = new Date(
        Math.round(submittedAt.getTime() / 1000) + props.ttl
    );
    const expiresIn = props.ttl;

    const sampleData: ActiveMention = {
        url: "https://beatonma.org",
        submitted_at: submittedAt,
        expires_at: expiresAt,
        expires_in: expiresIn,
        status: {
            successful: true,
            status_code: 202,
            message: "The target server accepted the webmention.",
            source_url: "/webmentions_tester/",
            target_url: "https://beatonma.org",
            endpoint: "https://beatonma.org/webmention/",
        },
    };

    return (
        <ActiveMentionUI
            mention={sampleData}
            className="webmention-tester-sample"
            label="Sample"
            expanded={props.expanded}
        />
    );
};

interface ActiveMentionProps extends HTMLAttributes<any> {
    requestUpdate?: (callback: () => void) => void;
    mention: ActiveMention;
    expanded: boolean;
    label?: string;
}
const ActiveMentionUI = (props: ActiveMentionProps) => {
    const [awaitingTask, setAwaitingTask] = useState(true);

    const { mention, className, requestUpdate, label, expanded } = props;
    const status = mention?.status;

    useEffect(() => {
        if (status === null && requestUpdate) {
            requestUpdate(() => setAwaitingTask(!awaitingTask));
        }
    }, [status, awaitingTask]);

    return (
        <div className={classes(className, "active-mention")}>
            <div className="header">
                <div>
                    <Label className="temp">{label}</Label>
                    <a href={`${mention.url}`}>{mention.url}</a>
                </div>

                <div>
                    <Label>
                        Expires: {formatTimeDelta(mention.expires_in)}
                    </Label>
                </div>
            </div>

            <MentionStatusUI status={status} expanded={expanded} />
        </div>
    );
};

interface MentionStatusProps {
    status?: MentionStatus;
    expanded: boolean;
}
const MentionStatusUI = (props: MentionStatusProps) => {
    const { status, expanded } = props;

    if (status === null) {
        return (
            <Row>
                <MaterialIcon className="refresh" icon={AppIcon.Refresh} />
                <div>Status unknown - please wait a moment...</div>
            </Row>
        );
    }

    const successMessage = status.successful ? (
        <Row>
            <MaterialIcon icon={AppIcon.CheckMark} />
            <span>Accepted by server</span>
        </Row>
    ) : (
        <Row>
            <MaterialIcon className="warn" icon={AppIcon.Close} />
            <span>Rejected by server</span>
        </Row>
    );

    return (
        <Dropdown header={successMessage} expandedDefault={expanded}>
            <table className="status">
                <tbody>
                    <StatusTableRow
                        label="Status"
                        content={status.status_code}
                    />
                    <StatusTableRow label="Message" content={status.message} />
                    <StatusTableRow
                        label="Source"
                        content={status.source_url}
                    />
                    <StatusTableRow
                        label="Target"
                        content={status.target_url}
                    />
                    <StatusTableRow
                        label="Endpoint"
                        content={status.endpoint}
                    />
                </tbody>
            </table>
        </Dropdown>
    );
};

interface StatusTableRowProps {
    label: string;
    content: any;
}

const StatusTableRow = (props: StatusTableRowProps) => {
    return (
        <tr>
            <td>
                <Label>{props.label}</Label>
            </td>
            <td>
                <code className="status-content">{props.content}</code>
            </td>
        </tr>
    );
};

interface CreateTempMentionProps {
    onSubmit: () => void;
}

const CreateTempMention = (props: CreateTempMentionProps) => {
    const [url, setUrl] = useState("");
    const [isError, setIsError] = useState(false);

    const post = () => {
        create(Endpoint, { url: url })
            .then(response => {
                if (response.status === 400) {
                    throw "Validation failure";
                }

                console.log(`OK ${JSON.stringify(response)}`);
                setUrl("");
                setIsError(false);
                props.onSubmit();
            })
            .catch(err => {
                console.error(err);
                setIsError(true);
            });
    };

    const onKeyPress = (event: KeyboardEvent) => {
        setIsError(false);
        if (event.key === "Enter") {
            event.preventDefault();
            post();
        }
    };

    return (
        <section>
            <h2>Temporary mentions</h2>
            <p>Submit a link to your content to test your Webmentions setup!</p>
            <ul>
                <li>
                    Your link will appear on this page for a while (until it
                    expires).
                </li>
                <li>
                    Your webmentions endpoint should immediately receive a
                    notification that this page has mentioned your page.
                </li>
            </ul>

            <form action="#">
                <input
                    type="url"
                    value={url}
                    onChange={e => setUrl(e.target.value)}
                    placeholder="https://yoursite.example/your-article/"
                    onKeyUp={onKeyPress}
                    autoFocus
                    required
                />
                <button type="submit" onClick={post}>
                    Submit
                </button>
                <ErrorMessage show={isError} />
            </form>

            <p>
                If your page mentions this page, it should appear{" "}
                <a href="#webmentions">below</a> in a few moments.
            </p>
        </section>
    );
};

interface ErrorMessageProps {
    show: boolean;
}
const ErrorMessage = (props: ErrorMessageProps) => {
    if (props.show) {
        return <div>Please check your URL - validation failed.</div>;
    } else {
        return null;
    }
};

const create = (url: string, data: any) =>
    fetch(url, {
        method: "POST",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
        },
        body: JSON.stringify(data),
    });

const Label = (props: HTMLAttributes<HTMLDivElement>) => {
    if (React.Children.count(props.children) === 0) return null;

    return (
        <div className={classes(props.className, "label")}>
            {props.children}
        </div>
    );
};
