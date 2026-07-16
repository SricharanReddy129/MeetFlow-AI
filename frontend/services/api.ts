import { auth } from "@clerk/nextjs/server";
import { DashboardData } from "../types/user";

// Fallback to localhost if the Vercel environment variable isn't injected yet
const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getUserDashboardData(): Promise<DashboardData | null> {
  if (!BACKEND_URL) {
    console.error("NEXT_PUBLIC_API_URL is not set");
    return null;
  }

  const { getToken } = await auth();
  const token = await getToken();

  try {
    const response = await fetch(`${BACKEND_URL}/api/users/me`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      cache: "no-store",
    });

    if (!response.ok) return null;
    return response.json();
  } catch (error) {
    console.error("Failed to fetch dashboard data:", error);
    return null;
  }
}