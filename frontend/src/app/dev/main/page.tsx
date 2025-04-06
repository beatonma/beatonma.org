import { Metadata } from "next";
import Layout from "@/app/(main)/layout";

export const metadata: Metadata = {
  title: "Base layout",
  description: "",
};

export default async function Page() {
  return (
    <Layout>
      <div>main layout.tsx</div>
    </Layout>
  );
}
