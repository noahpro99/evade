import { useState } from "react";
import {
  Home,
  FileText,
  Phone,
  Shield,
  Heart,
  MapPin,
  Edit,
  History,
  Bell,
  Users,
  Camera,
  Battery,
  Wifi,
  Plus,
  Trash2,
  Settings,
} from "lucide-react";

const App = () => {
  const [isAdultMode, setIsAdultMode] = useState(true);
  const [activeTab, setActiveTab] = useState("home");

  // Detection History Data
  const [detectionHistory] = useState([
    {
      id: 1,
      name: "John Smith",
      riskLevel: "High",
      tier: "Tier 3",
      conviction: "Sexual assault (2019)",
      photo:
        "https://www.vspsor.com/api/file/image/019daa4c-b6c9-4f26-aff8-088ae5b1315d",
      timestamp: "2:45 PM - Today",
      location: "Main St & 5th Ave",
    },
    {
      id: 2,
      name: "Mike Johnson",
      riskLevel: "Medium",
      tier: "Tier 2",
      conviction: "Indecent exposure (2020)",
      photo:
        "https://www.vspsor.com/api/file/image/1cca91b7-020e-481d-8f78-e5afbf84bf94",
      timestamp: "11:30 AM - Today",
      location: "Central Park",
    },
  ]);

  // Alert Settings
  const [alertSettings, setAlertSettings] = useState({
    sensitivity: "Medium",
    instantNotifications: true,
    soundAlerts: true,
    vibrationAlerts: true,
    emailNotifications: false,
    autoCallPolice: false,
  });

  // Emergency Contacts
  const [emergencyContacts] = useState([
    {
      id: 1,
      name: "Sarah Johnson",
      phone: "(555) 123-4567",
      relation: "Mother",
      primary: true,
    },
    {
      id: 2,
      name: "Mike Johnson",
      phone: "(555) 987-6543",
      relation: "Father",
      primary: false,
    },
  ]);

  const ModeToggle = () => (
    <div className="bg-white border border-white rounded-full p-1 shadow-sm">
      <div className="flex relative">
        <button
          onClick={() => setIsAdultMode(true)}
          className={`px-4 py-2 rounded-full text-sm font-medium transition-all flex items-center space-x-2 ${
            isAdultMode
              ? "bg-dark text-white shadow-sm"
              : "text-dark hover:text-dark hover:bg-white"
          }`}
        >
          <Shield className="w-4 h-4" />
          <span>Adult</span>
        </button>
        <button
          onClick={() => setIsAdultMode(false)}
          className={`px-4 py-2 rounded-full text-sm font-medium transition-all flex items-center space-x-2 ${
            !isAdultMode
              ? "bg-dark text-white shadow-sm"
              : "text-dark hover:text-dark hover:bg-white"
          }`}
        >
          <Heart className="w-4 h-4" />
          <span>Kid</span>
        </button>
      </div>
    </div>
  );

  // Main Dashboard Page
  const DashboardPage = () => (
    <div className="space-y-6">
      {/* Device Status */}
      <div className="bg-white border border-white rounded-3xl shadow-sm p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-dark">EVADE Device Status</h2>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-dark rounded-full animate-pulse"></div>
            <span className="text-sm font-medium text-dark">Connected</span>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div className="bg-white rounded-xl p-4 text-center">
            <Battery className="w-6 h-6 text-dark mx-auto mb-2" />
            <div className="text-sm font-medium text-dark">Battery</div>
            <div className="text-lg font-bold text-dark">87%</div>
          </div>
          <div className="bg-white rounded-xl p-4 text-center">
            <Wifi className="w-6 h-6 text-dark mx-auto mb-2" />
            <div className="text-sm font-medium text-dark">Connection</div>
            <div className="text-sm font-bold text-dark">Strong</div>
          </div>
          <div className="bg-white rounded-xl p-4 text-center">
            <Camera className="w-6 h-6 text-dark mx-auto mb-2" />
            <div className="text-sm font-medium text-dark">Mode</div>
            <div className="text-sm font-bold text-dark">
              {isAdultMode ? "Adult" : "Kid"}
            </div>
          </div>
        </div>
      </div>

      {/* Auto-Call Police Section - Only for Adult Mode */}
      {isAdultMode && (
        <div className="bg-white border border-white rounded-3xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-dark">Emergency Response</h3>
            <span className="text-sm text-dark bg-white px-2 py-1 rounded-full">
              Adult Mode
            </span>
          </div>
          <div className="bg-white border border-white rounded-xl p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <Phone className="w-5 h-5 text-dark" />
                <div>
                  <span className="text-dark font-medium">
                    Auto-Call Police
                  </span>
                  <p className="text-sm text-dark mt-1">
                    Automatically contact authorities when high-risk offender
                    detected
                  </p>
                </div>
              </div>
              <div className="flex items-center bg-white border border-dark rounded-full p-1">
                <button
                  onClick={() =>
                    setAlertSettings({
                      ...alertSettings,
                      autoCallPolice: false,
                    })
                  }
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                    !alertSettings.autoCallPolice
                      ? "bg-dark text-white"
                      : "text-dark hover:bg-white"
                  }`}
                >
                  Off
                </button>
                <button
                  onClick={() =>
                    setAlertSettings({
                      ...alertSettings,
                      autoCallPolice: true,
                    })
                  }
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                    alertSettings.autoCallPolice
                      ? "bg-dark text-white"
                      : "text-dark hover:bg-white"
                  }`}
                >
                  On
                </button>
              </div>
            </div>
            {alertSettings.autoCallPolice && (
              <div className="mt-4 p-3 bg-white rounded-lg">
                <div className="flex items-start space-x-2">
                  <Shield className="w-4 h-4 text-dark mt-0.5" />
                  <div className="text-sm text-dark">
                    <p className="font-medium">Emergency Protocol Active</p>
                    <p className="mt-1">
                      When a Tier 3 offender is detected, emergency services
                      will be contacted automatically with your location and
                      offender details.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Recent Activity */}
      <div className="bg-white border border-white rounded-3xl shadow-sm p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-dark">Recent Activity</h3>
          <button
            onClick={() => setActiveTab("history")}
            className="text-dark text-sm font-medium hover:text-dark"
          >
            View All
          </button>
        </div>

        <div className="space-y-3">
          {detectionHistory.slice(0, 2).map((detection) => (
            <div
              key={detection.id}
              className="flex items-center space-x-3 p-3 bg-white rounded-xl"
            >
              <img
                className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center text-sm"
                src={detection.photo}
                alt={detection.name}
              />
              <div className="flex-1">
                <div className="font-medium text-dark">{detection.name}</div>
                <div className="text-sm text-dark">
                  {detection.riskLevel} Risk • {detection.timestamp}
                </div>
              </div>
              <div
                className={`px-2 py-1 rounded-full text-xs font-medium bg-white text-dark`}
              >
                {detection.tier}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  // Detection History Page
  const DetectionHistoryPage = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <div className="inline-flex items-center space-x-2 bg-white border border-white rounded-full px-4 py-2 mb-4 shadow-sm">
          <History className="w-4 h-4 text-dark" />
          <span className="text-sm font-medium text-dark">Detection Log</span>
        </div>
        <h2 className="text-2xl font-bold text-dark mb-2">Recent Detections</h2>
        <p className="text-dark">Offenders detected by your EVADE system</p>
      </div>

      <div className="space-y-4">
        {detectionHistory.map((detection) => (
          <div
            key={detection.id}
            className="bg-white border border-white rounded-2xl shadow-sm p-6"
          >
            <div className="flex items-start space-x-4">
              <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center text-2xl">
                {detection.photo}
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-bold text-dark">{detection.name}</h3>
                  <div
                    className={`px-3 py-1 rounded-full text-xs font-medium bg-white text-dark`}
                  >
                    {detection.riskLevel} Risk
                  </div>
                </div>
                <div className="space-y-1 mb-3">
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-dark">Tier:</span>
                    <span className="text-sm text-dark">{detection.tier}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-dark">
                      Conviction:
                    </span>
                    <span className="text-sm text-gray-800">
                      {detection.conviction}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <MapPin className="w-4 h-4 text-dark" />
                    <span className="text-sm text-dark">
                      {detection.location}
                    </span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-dark">
                    {detection.timestamp}
                  </span>
                  <button className="text-dark text-sm font-medium hover:text-dark">
                    View Details
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  // Alert Settings & Contacts Page
  const AlertSettingsPage = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-dark mb-2">Settings</h2>
      </div>

      <div className="flex justify-center mb-8">
        <ModeToggle />
      </div>

      <div className="space-y-4">
        <div className="bg-white border border-white rounded-2xl shadow-sm p-6">
          <h3 className="font-semibold text-dark mb-4">
            Detection Sensitivity
          </h3>
          <div className="flex items-center bg-white border border-dark rounded-full p-1">
            {["Low", "Medium", "High"].map((level) => (
              <button
                key={level}
                onClick={() =>
                  setAlertSettings({ ...alertSettings, sensitivity: level })
                }
                className={`px-4 py-2 rounded-full text-sm font-medium transition-all flex-1 ${
                  alertSettings.sensitivity === level
                    ? "bg-dark text-white"
                    : "text-dark hover:bg-white"
                }`}
              >
                {level}
              </button>
            ))}
          </div>
        </div>

        <div className="bg-white border border-white rounded-2xl shadow-sm p-6">
          <h3 className="font-semibold text-dark mb-4">Notification Types</h3>
          <div className="space-y-4">
            {[
              {
                key: "instantNotifications",
                label: "Instant Push Notifications",
                icon: Bell,
              },
              { key: "soundAlerts", label: "Sound Alerts", icon: Bell },
              {
                key: "vibrationAlerts",
                label: "Vibration Alerts",
                icon: Phone,
              },
              {
                key: "emailNotifications",
                label: "Email Notifications",
                icon: FileText,
              },
            ].map(({ key, label, icon: Icon }) => (
              <div key={key} className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <Icon className="w-5 h-5 text-dark" />
                  <span className="text-dark">{label}</span>
                </div>
                <button
                  onClick={() =>
                    setAlertSettings({
                      ...alertSettings,
                      [key]: !alertSettings[key as keyof typeof alertSettings],
                    })
                  }
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    alertSettings[key as keyof typeof alertSettings]
                      ? "bg-dark"
                      : "bg-white"
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      alertSettings[key as keyof typeof alertSettings]
                        ? "translate-x-6"
                        : "translate-x-1"
                    }`}
                  />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Emergency Contacts Section - Only for Kid Mode */}
        {!isAdultMode && (
          <div className="bg-white border border-white rounded-2xl shadow-sm p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-semibold text-dark">Emergency Contacts</h3>
              <span className="text-sm text-dark bg-white px-2 py-1 rounded-full">
                Kid Mode
              </span>
            </div>

            <div className="space-y-4 mb-6">
              {emergencyContacts.map((contact) => (
                <div
                  key={contact.id}
                  className="bg-white border border-white rounded-xl p-4"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div
                        className={`w-10 h-10 rounded-full flex items-center justify-center bg-white text-dark`}
                      >
                        <Users className="w-5 h-5" />
                      </div>
                      <div>
                        <div className="flex items-center space-x-2">
                          <h4 className="font-medium text-dark">
                            {contact.name}
                          </h4>
                          {contact.primary && (
                            <span className="bg-white text-dark text-xs px-2 py-1 rounded-full">
                              Primary
                            </span>
                          )}
                        </div>
                        <p className="text-sm text-dark">{contact.phone}</p>
                        <p className="text-xs text-dark">{contact.relation}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-1">
                      <button className="p-1.5 text-dark hover:text-dark hover:bg-white rounded-lg transition-all">
                        <Edit className="w-3.5 h-3.5" />
                      </button>
                      <button className="p-1.5 text-dark hover:text-dark hover:bg-white rounded-lg transition-all">
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <button className="w-full bg-white border-2 border-dashed border-white rounded-xl p-4 text-dark hover:bg-white transition-all">
              <div className="flex items-center justify-center space-x-2">
                <Plus className="w-4 h-4" />
                <span className="font-medium">Add Emergency Contact</span>
              </div>
            </button>
          </div>
        )}
      </div>
    </div>
  );

  const renderContent = () => {
    switch (activeTab) {
      case "home":
        return <DashboardPage />;
      case "history":
        return <DetectionHistoryPage />;
      case "alerts":
        return <AlertSettingsPage />;
      default:
        return <DashboardPage />;
    }
  };

  return (
    <div className="min-h-screen bg-white flex flex-col">
      {/* Subtle background pattern */}
      <div className="absolute inset-0 opacity-30">
        <div
          className="absolute inset-0"
          style={{
            backgroundImage:
              "radial-gradient(circle at 1px 1px, rgba(55, 69, 69, 0.1) 1px, transparent 0)",
            backgroundSize: "20px 20px",
          }}
        ></div>
      </div>

      {/* Header */}
      <header className="relative bg-white border-b border-white shadow-sm backdrop-blur-sm">
        <div className="max-w-6xl mx-auto flex items-center justify-between p-6">
          <img src="/logo.png" alt="EVADE" className="w-12 h-12" />
          <img src="/name.png" alt="EVADE" className="h-8" />
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 flex-1 max-w-4xl mx-auto w-full p-6 py-12 pb-24">
        {renderContent()}
      </main>

      {/* Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-white shadow-sm backdrop-blur-sm z-50">
        <div className="max-w-6xl mx-auto px-6">
          <div className="flex justify-around py-4">
            {[
              { id: "home", icon: Home, label: "Dashboard" },
              { id: "history", icon: History, label: "Detections" },
              { id: "alerts", icon: Settings, label: "Settings" },
            ].map(({ id, icon: Icon, label }) => (
              <button
                key={id}
                onClick={() => setActiveTab(id)}
                className={`flex flex-col items-center space-y-2 px-8 py-3 rounded-xl transition-all ${
                  activeTab === id
                    ? "bg-white shadow-sm border border-white"
                    : "hover:bg-white"
                }`}
              >
                <Icon className={`w-5 h-5 text-dark`} />
                <span className={`text-xs font-medium text-dark`}>{label}</span>
              </button>
            ))}
          </div>
        </div>
      </nav>
    </div>
  );
};

export default App;
