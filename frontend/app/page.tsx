import { SignInButton, SignUpButton, UserButton } from "@clerk/nextjs";
import { auth } from "@clerk/nextjs/server";

export default async function Home() {
  const { userId } = await auth();

  return (
    <main className="landing-shell">
      <section className="hero-card">
        <div className="hero-badge">MeetFlow AI</div>
        <h1>Clean meetings. Clear outcomes.</h1>
        <p className="hero-copy">
          Upload meeting audio, get structured summaries, and keep every decision easy to revisit.
        </p>

        <div className="hero-points" aria-label="Product highlights">
          <span>Fast uploads</span>
          <span>Readable summaries</span>
          <span>Simple history</span>
        </div>

        <div className="hero-action-row">
          {!userId ? (
            <>
              <SignInButton mode="modal">
                <button className="primary-button">Sign In</button>
              </SignInButton>

              <SignUpButton mode="modal">
                <button className="secondary-button">Sign Up</button>
              </SignUpButton>
            </>
          ) : (
            <>
              <div className="signed-in-note">You are securely logged in.</div>
              <UserButton />
            </>
          )}
        </div>
      </section>

      <aside className="hero-panel" aria-label="Preview">
        <div className="panel-card">
          <div className="panel-kicker">Today</div>
          <div className="panel-title">Meeting summary preview</div>
          <div className="panel-item">
            <span>Action items</span>
            <strong>3</strong>
          </div>
          <div className="panel-item">
            <span>Key decisions</span>
            <strong>5</strong>
          </div>
          <div className="panel-item">
            <span>Follow-ups</span>
            <strong>2</strong>
          </div>
        </div>
      </aside>
    </main>
  );
}