export async function HEAD(request: Request) {
  return new Response(undefined, {
    status: 204,
  });
}
