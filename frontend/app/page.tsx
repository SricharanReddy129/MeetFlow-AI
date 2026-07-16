import { SignInButton, SignUpButton, UserButton } from "@clerk/nextjs";
import { auth } from "@clerk/nextjs/server";

export default async function Home() {
  // Check the authentication state directly on the server
  const { userId } = await auth();

  return (
    <main style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: "100vh", fontFamily: "sans-serif" }}>
      <h1>Welcome to the App</h1>
      
      {!userId ? (
        <>
          {/* Render this if the user is NOT logged in */}
          <p style={{ marginBottom: "20px" }}>Please sign in or sign up to continue.</p>
          <div style={{ display: "flex", gap: "10px" }}>
            <SignInButton mode="modal">
              <button style={{ padding: "10px 20px", cursor: "pointer" }}>Sign In</button>
            </SignInButton>
            
            <SignUpButton mode="modal">
              <button style={{ padding: "10px 20px", cursor: "pointer" }}>Sign Up</button>
            </SignUpButton>
          </div>
        </>
      ) : (
        <>
          {/* Render this if the user IS logged in */}
          <p style={{ marginBottom: "20px" }}>You are securely logged in!</p>
          <UserButton />
        </>
      )}
    </main>
  );
}