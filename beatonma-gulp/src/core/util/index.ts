export const measurePerformance = (func: () => void, repeats: number = 1) => {
    const start = performance.now();

    for (let i = 0; i < repeats; i++) {
        func();
    }
    const end = performance.now();
    const meanDuration = (end - start) / repeats;
    console.log(`${meanDuration}ms (n=${repeats})`);
};
