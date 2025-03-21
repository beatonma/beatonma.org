import { schemas } from "@/api";

export type PostPreview = schemas["PostPreview"];
export type PostDetail = schemas["PostDetail"];
export type Post = PostPreview | PostDetail;

export type Webmention = schemas["Mention"];
