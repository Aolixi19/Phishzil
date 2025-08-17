import Topbar from "./Topbar";
import Sidebar from "./Sidebar";

const Layout = ({ children }) => {
  return (
    <div className="flex flex-col min-h-screen">
      <Topbar />
      <div className="flex flex-1 pt-16"> {/* pt-16 accounts for topbar height */}
        <Sidebar />
        <main className="flex-1 ml-64 p-6"> {/* ml-64 matches sidebar width */}
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;