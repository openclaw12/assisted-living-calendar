import { EngagementFeed } from "../../components/EngagementFeed";
import { ScheduleTimeline } from "../../components/ScheduleTimeline";
import { PollBuilder } from "../../components/PollBuilder";
import "../../styles/dashboard.css";

export function Dashboard() {
  return (
    <main className="dashboard">
      <section>
        <h1>Community Pulse</h1>
        <EngagementFeed />
      </section>
      <section>
        <h2>Upcoming Highlights</h2>
        <ScheduleTimeline />
      </section>
      <section>
        <h2>Plan Next Month</h2>
        <PollBuilder />
      </section>
    </main>
  );
}
