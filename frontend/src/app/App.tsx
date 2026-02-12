import { BrowserRouter, Route, Routes } from "react-router-dom";

import { BusinessPortal } from "./business/BusinessPortal";
import { EmployeeApp } from "./employee/EmployeeApp";
import { ResidentApp } from "./resident/ResidentApp";
import { SignupPage } from "./auth/SignupPage";
import { Dashboard } from "./dashboard/Dashboard";

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/portal/*" element={<BusinessPortal />} />
        <Route path="/employee/*" element={<EmployeeApp />} />
        <Route path="/resident/*" element={<ResidentApp />} />
        <Route path="/signup/:orgSlug/:role" element={<SignupPage />} />
        <Route path="/*" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
