import { UserButton } from "@clerk/nextjs";
import { auth, currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { getUserAccountData } from "../../services/api";

export default async function Dashboard() {
  const { userId } = await auth();

  if (!userId) {
    redirect("/");
  }

  const user = await currentUser();
  
  // Call your FastAPI backend!
  const dbAccount = await getUserAccountData();

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif" }}>
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "1px solid #ccc", paddingBottom: "20px" }}>
        <h1>My Dashboard</h1>
        <UserButton />
      </header>

      <main style={{ marginTop: "40px" }}>
        <h2>Welcome back, {user?.firstName}!</h2>
        
        {/* Render data directly from your database */}
        <div style={{ marginTop: "20px", padding: "20px", background: "#f5f5f5", borderRadius: "8px" }}>
          <h3>Account Status</h3>
          {dbAccount ? (
             <p>Your current plan: <strong>{dbAccount.tier}</strong></p>
          ) : (
             <p style={{ color: "red" }}>Could not connect to the backend database.</p>
          )}
        </div>
      </main>
    </div>
  );
}