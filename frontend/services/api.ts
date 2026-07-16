import { auth } from "@clerk/nextjs/server";

export async function getUserAccountData() {
  // 1. Grab the Clerk session token from the Next.js server
  const { getToken } = await auth();
  const token = await getToken();

  if (!token) {
    throw new Error("No authentication token found");
  }

  // 2. Make the request to your FastAPI backend, attaching the token
  // (Replace with your actual Railway backend URL in production)
  const response = await fetch("http://localhost:8000/api/users/me", {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    // Prevent Next.js from caching this specific request so the dashboard is always fresh
    cache: "no-store", 
  });

  if (!response.ok) {
    return null;
  }

  return response.json();
}