import { Metadata } from "next";
import SampleSearch from "@/app/(main)/dev/search/search";

export const metadata: Metadata = {
  title: "Search",
  description: "",
};

export default async function Page() {
  return <SampleSearch />;
}
