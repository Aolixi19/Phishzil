import { Routes, Route } from "react-router-dom";
import Home from "./pages/home";
import Register from "./pages/auths/register";
import Login from "./pages/auths/login";
import ForgotPassword from "./pages/auths/forgot_password";
import Dashboard from "./pages/urls/dashboard";
import Scanner from "./pages/urls/Scanner";
import Urls from "./pages/urls/Urls";
import Emails from "./pages/urls/Emails";
import Files from "./pages/urls/Files";
import Reports from "./pages/urls/Reports";
import Settings from "./layout/Settings";
import Phlink from "./process_1/phLink.jsx"; 
import PhEmail from "./process_1/phEmail.jsx";
import PhFile from "./process_1/phFile.jsx";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/signup" element={<Register />} />
      <Route path="/login" element={<Login />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />

      {/* Sidebar Routes */}
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/safe-view" element={<Scanner />} />
      <Route path="/url-scanner" element={<Urls />} />
      <Route path="/email-scanner" element={<Emails />} />
      <Route path="/file-scanner" element={<Files />} />
      <Route path="/reports" element={<Reports />} />
      <Route path="/settings" element={<Settings />} />

      {/* Disarming Process Pages */}
      <Route path="/phlink" element={<Phlink />} /> 
      <Route path="/ph-email" element={<PhEmail />} />
        <Route path="/ph-file" element={<PhFile />} />
      
    </Routes>
  );
}

export default App;