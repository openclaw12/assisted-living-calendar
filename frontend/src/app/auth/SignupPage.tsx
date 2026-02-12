import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

interface Organization {
  id: string;
  name: string;
}

export function SignupPage() {
  const { orgSlug = "", role = "" } = useParams();
  const [organization, setOrganization] = useState<Organization | null>(null);
  const [status, setStatus] = useState<string>("Loading...");

  useEffect(() => {
    async function loadOrg() {
      try {
        const res = await fetch(`/api/organizations/slug/${orgSlug}`);
        if (!res.ok) throw new Error("Organization not found");
        const data = (await res.json()) as Organization;
        setOrganization(data);
        setStatus("");
      } catch (err) {
        setStatus((err as Error).message);
      }
    }
    loadOrg();
  }, [orgSlug]);

  if (status) {
    return <p>{status}</p>;
  }

  return (
    <div className="signup">
      <h1>Sign up for {organization?.name}</h1>
      <p>Role selected: {role}</p>
      <form>
        <label>
          Email
          <input type="email" name="email" required />
        </label>
        <label>
          Password
          <input type="password" name="password" required />
        </label>
        <label>
          Display name
          <input type="text" name="display_name" required />
        </label>
        <button type="submit">Create account</button>
      </form>
    </div>
  );
}
