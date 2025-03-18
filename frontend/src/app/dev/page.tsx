import { Row } from "@/components/layout";
import ThemeController from "@/components/themed/light-dark";
import * as Preview from "./_components";

export default function Page() {
  return (
    <main className="mx-auto column gap-16 mb-16 items-center">
      <div className="readable">
        <Row className="justify-between">
          <h1>Components overview</h1>
          <ThemeController />
        </Row>

        <Preview.Buttons />
        <Preview.Icons />
        <Preview.Loaders />
      </div>
      <Preview.Media />
    </main>
  );
}
