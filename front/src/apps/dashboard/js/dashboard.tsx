import React, { ReactNode } from "react";
import { useEffect, useState } from "react";
import { formatDate } from "../../main/js/util/datetime";
import { createRoot } from "react-dom/client";

const DashboardApp = () => {
    const root = createRoot(document.getElementById("dashboard_wrapper"));
    root.render(<Dashboard />);
};

interface SystemStatus {
    uptime: string;
}

interface GithubStatus {
    cached_at: string;
}

interface HCard {
    name: string;
    avatar: string;
    homepage: string;
}

interface WebMentionData {
    hcard?: HCard;
    quote?: string;
    source_url: string;
    target_url: string;
    published: string;
    type: string;
}

interface WebmailData {
    name: string;
    contact: string;
    body: string;
    timestamp: string;
}

interface PageViewData {
    url: string;
    timestamp: string;
    ip: string;
    device: string;
    os: string;
    browser: string;
    count?: number;
}

interface DashboardStatus {
    system: SystemStatus;
    github: GithubStatus;
    mentions: WebMentionData[];
    webmail: WebmailData[];
    views: PageViewData[];
}

const Dashboard = () => {
    const [status, setStatus] = useState<DashboardStatus>(null);

    useEffect(() => {
        document.title = "Dashboard";
        fetch("status/", { method: "GET" })
            .then(response => response.json())
            .then(setStatus);
    }, []);

    if (status == null) return null;

    return (
        <>
            <h1>Dashboard</h1>
            <System status={status.system} />
            <Github status={status.github} />
            <div id="dashboard">
                <RecentViews views={status.views} />
                <RecentMentions mentions={status.mentions} />
                <RecentWebmail webmail={status.webmail} />
            </div>
            <Footer />
        </>
    );
};

interface GithubProps {
    status: GithubStatus;
}

const Github = (props: GithubProps) => {
    return (
        <div className="github">
            <span>
                <TimeStamp
                    label="Github cached at"
                    timestamp={props.status.cached_at}
                />
            </span>
        </div>
    );
};

interface SystemProps {
    status: SystemStatus;
}

const System = (props: SystemProps) => {
    return <div className="system">Uptime {props.status.uptime}</div>;
};

interface RecentMentionsProps {
    mentions: WebMentionData[];
}

const RecentMentions = (props: RecentMentionsProps) => {
    return (
        <Group title="Recent mentions">
            {props.mentions.map(mention => (
                <Mention key={mention.published} mention={mention} />
            ))}
        </Group>
    );
};

interface MentionProps {
    mention: WebMentionData;
}

const Mention = (props: MentionProps) => {
    const { mention } = props;
    const source = new URL(mention.source_url);
    const target = new URL(mention.target_url);

    return (
        <div className="mention">
            <div className="row">
                <div className="hcard" title={mention.hcard?.name}>
                    <OptionalLink url={mention.hcard?.homepage}>
                        <div
                            className="avatar"
                            style={{
                                backgroundImage: `url(${
                                    mention.hcard?.avatar ||
                                    "/static/images/icon/ic_no-avatar.svg"
                                })`,
                            }}
                        ></div>
                    </OptionalLink>
                </div>
                <div>
                    <TimeStamp timestamp={mention.published} />
                    <div className="row">
                        <Url href={source.href} className="wm-source">
                            {source.hostname}
                        </Url>{" "}
                        <span className="material-symbols-outlined">
                            keyboard_arrow_right
                        </span>{" "}
                        <Url href={target.href} className="wm-target">
                            {target.pathname}
                        </Url>
                    </div>
                </div>
            </div>
        </div>
    );
};

interface OptionalLinkProps {
    url: string;
    children: ReactNode | ReactNode[];
}

const OptionalLink = (props: OptionalLinkProps) => {
    const { url, children, ...rest } = props;
    if (url) {
        return <a href={url} {...rest} />;
    } else return <>{children}</>;
};

interface RecentViewsProps {
    views: PageViewData[];
}

const RecentViews = (props: RecentViewsProps) => {
    const [views, setViews] = useState([]);

    useEffect(() => {
        const collapsed = props.views.reduce((acc, x) => {
            if (acc.length === 0) {
                x.count = 1;
                acc.push(x);
                return acc;
            }
            const previous = acc.slice(-1)[0];
            if (previous.url === x.url) {
                previous.count += 1;
            } else {
                x.count = 1;
                acc.push(x);
            }
            return acc;
        }, []);
        setViews(collapsed);
    }, [props.views]);

    return (
        <Group title="Recent page views">
            {views.map(view => (
                <PageView view={view} key={view.timestamp} />
            ))}
        </Group>
    );
};

interface PageViewProps {
    view: PageViewData;
}

const PageView = (props: PageViewProps) => {
    const view = props.view;
    const url = new URL(view.url);

    return (
        <a href={view.url}>
            <div
                key={view.timestamp}
                className="page-view v1-row"
                title={`${view.device} | ${view.os} | ${view.browser}: ${view.ip}`}
            >
                <TimeStamp timestamp={view.timestamp} />
                <Url>{url.pathname}</Url>
                {view.count > 1 ? (
                    <div className="count">✕{view.count}</div>
                ) : (
                    <></>
                )}
            </div>
        </a>
    );
};

interface RecentWebmailProps {
    webmail: WebmailData[];
}

const RecentWebmail = (props: RecentWebmailProps) => {
    return (
        <Group title="Recent mail">
            {props.webmail.map(mail => (
                <Webmail mail={mail} key={mail.timestamp} />
            ))}
        </Group>
    );
};

interface WebmailProps {
    mail: WebmailData;
}

const Webmail = (props: WebmailProps) => {
    const { mail } = props;

    return (
        <div
            className="webmail"
            title={`From ${mail.name} | Contact: ${mail.contact}`}
        >
            <TimeStamp timestamp={mail.timestamp} />
            <div className="row">
                <div className="webmail-name">{mail.name}</div>
                <div className="webmail-contact">{mail.contact}</div>
            </div>
            <div className="webmail-body">
                <LinkifyText>{mail.body}</LinkifyText>
            </div>
        </div>
    );
};

interface UrlProps {
    href?: string;
    className?: string;
    children: string;
}

const Url = (props: UrlProps) => {
    const parts = props.children
        .replace("www.", "")
        .replace(".com", "")
        .split("");

    return (
        <OptionalLink url={props.href}>
            <div className={`url ${props.className || ""}`}>
                {parts.map((x, index) => {
                    if (x === "/")
                        return (
                            <span className="slash" key={index}>
                                {x}
                            </span>
                        );
                    else return <>{x}</>;
                })}
            </div>
        </OptionalLink>
    );
};

interface LinkfyTextProps {
    children: string;
}

const LinkifyText = (props: LinkfyTextProps) => {
    const [linkified, setLinkified] = useState(null);
    const pattern = /((?:https?:\/\/)?(?:[\w-_.]+\.[\w-_./]+))/g;

    useEffect(() => {
        const split = props.children.split(pattern);

        setLinkified(
            split.map(x => {
                if (x.match(pattern)) {
                    const fixedUrl = x.startsWith("http") ? x : `https://${x}`;
                    try {
                        const url = new URL(fixedUrl);
                        return (
                            <>
                                [
                                <a
                                    className="linkified"
                                    title={url.href}
                                    href={url.href}
                                >
                                    {url.hostname}
                                </a>
                                ]
                            </>
                        );
                    } catch (e) {
                        console.log(`URL parsing error: ${x}: ${e}`);
                    }

                    return x;
                } else {
                    return x;
                }
            })
        );
    }, [props.children]);

    return <>{linkified}</>;
};

interface GroupProps {
    title: string;
    children: ReactNode | ReactNode[];
}

const Group = (props: GroupProps) => {
    return (
        <div className="group">
            <h3>{props.title}</h3>
            <div className="group-content">{props.children}</div>
        </div>
    );
};

interface TimestampProps {
    timestamp: string;
    label?: string;
}

const TimeStamp = (props: TimestampProps) => {
    const timestamp = new Date(props.timestamp);

    const _date = formatDate(timestamp, {
        day: "numeric",
        month: "short",
        year: "numeric",
    });
    const date = _date === "Today" ? "" : _date;
    const time = timestamp.toLocaleTimeString("en-GB", {
        hour: "2-digit",
        minute: "2-digit",
    });

    return (
        <time className="timestamp" dateTime={props.timestamp}>
            {props.label} {date} {time}
        </time>
    );
};

const Footer = () => {
    return <footer></footer>;
};

DashboardApp();
