import { Row } from "@/components/layout";
import ThemeController from "@/components/themed/light-dark";
import { Buttons, Icons, Loaders } from "./components";

export default function Page() {
  return (
    <main className="readable mx-auto column gap-16">
      <Row className="justify-between">
        <h1>Components overview</h1>
        <ThemeController />
      </Row>

      <Buttons />
      <Icons />
      <Loaders />
    </main>
  );
}
