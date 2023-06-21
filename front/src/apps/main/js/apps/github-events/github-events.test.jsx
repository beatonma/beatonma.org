import { filterEvents } from "./github-events";
import { SampleEvents } from "./github-events.testdata";

test("Events are grouped by private/public and by repository.", () => {
    const grouped = filterEvents(SampleEvents);

    expect(grouped.length).toBe(5);

    const first = grouped[0];
    expect(first.wikiEditEvents.length).toBe(2);
    expect(first.wikiEditEvents[0].action).toBe("edited");
    expect(first.wikiEditEvents[1].action).toBe("created");
});
