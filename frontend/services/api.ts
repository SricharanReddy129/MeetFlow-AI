import { auth } from "@clerk/nextjs/server";
import { DashboardData } from "../types/user";

export async function getUserDashboardData(): Promise<DashboardData | null> {
  const { getToken } = await auth();
  const token = await getToken();

  const response = await fetch("http://localhost:8000/api/users/me", {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    cache: "no-store",
  });

  if (!response.ok) return null;
  return response.json();
}