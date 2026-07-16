// frontend/services/paymentApi.ts
export async function createRazorpayOrder(token: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/payments/create-order`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}` },
  });
  return res.json();
}

export async function verifyRazorpayPayment(
  token: string,
  data: { order_id: string; payment_id: string; signature: string }
) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/payments/verify`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return res.json();
}