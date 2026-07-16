"use client";

import { useAuth } from "@clerk/nextjs";
import Script from "next/script";
import { createRazorpayOrder, verifyRazorpayPayment } from "../services/paymentApi";

declare global {
  interface Window {
    Razorpay: any;
  }
}

export default function UpgradeButton() {
  const { getToken } = useAuth();

  async function handleUpgradeClick() {
    const token = await getToken();
    if (!token) {
      alert("Please log in again.");
      return;
    }

    const order = await createRazorpayOrder(token);
    if (!order.order_id) {
      alert("Could not start payment. Please try again.");
      return;
    }

    const options = {
      key: order.key_id,
      amount: order.amount,
      currency: order.currency,
      order_id: order.order_id,
      name: "MeetFlow AI",
      description: "Upgrade to Pro",
      handler: async function (response: any) {
        const freshToken = await getToken(); // fresh token, in case the original expired during checkout
        if (!freshToken) {
          alert("Session expired. Please log in again.");
          return;
        }

        const result = await verifyRazorpayPayment(freshToken, {
          order_id: response.razorpay_order_id,
          payment_id: response.razorpay_payment_id,
          signature: response.razorpay_signature,
        });

        if (result.status === "success") {
          window.location.reload();
        } else {
          alert("Payment verification failed. Please contact support.");
        }
      },
      theme: { color: "#000000" },
    };

    const rzp = new window.Razorpay(options);
    rzp.open();
  }

  return (
    <>
      <Script src="https://checkout.razorpay.com/v1/checkout.js" strategy="lazyOnload" />
      <button style={{ marginTop: "10px" }} onClick={handleUpgradeClick}>
        Upgrade to PRO
      </button>
    </>
  );
}