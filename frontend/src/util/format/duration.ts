const SecondsInMinute = 60;
const SecondsInHours = SecondsInMinute * 60;

const zeroPad = (num: number): string => num.toString().padStart(2, "0");

/**
 * Format seconds as a duration.
 *
 * Hours are only displayed if non-zero. Minutes and seconds are always displayed.
 * The first component is not zero-padded, but all trailing components are.
 */
export const formatMediaDuration = (totalSeconds: number): string => {
  const hours = Math.floor(totalSeconds / SecondsInHours);
  let remainingSeconds = totalSeconds % SecondsInHours;

  let minutes = Math.floor(remainingSeconds / SecondsInMinute);
  remainingSeconds = remainingSeconds % SecondsInMinute;

  if (hours === 0) {
    return `${minutes}:${zeroPad(remainingSeconds)}`;
  }
  return `${hours}:${zeroPad(minutes)}:${zeroPad(remainingSeconds)}`;
};
