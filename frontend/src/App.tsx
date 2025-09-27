import React, { useState } from "react";
import {
  Home,
  FileText,
  Eye,
  Phone,
  Shield,
  Heart,
  CheckCircle,
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
      photo: "👤",
      timestamp: "2:45 PM - Today",
      location: "Main St & 5th Ave",
    },
    {
      id: 2,
      name: "Mike Johnson",
      riskLevel: "Medium",
      tier: "Tier 2",
      conviction: "Indecent exposure (2020)",
      photo: "👤",
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
  const [emergencyContacts, setEmergencyContacts] = useState([
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

  const LogoComponent = () => (
    <div className="flex items-center space-x-3">
      <div className="relative">
        <div className="w-12 h-12 bg-white/90 rounded-full shadow-sm border border-gray-200/50 flex items-center justify-center">
          <Eye className="w-6 h-6 text-blue-600" />
        </div>
        <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white flex items-center justify-center">
          <CheckCircle className="w-2.5 h-2.5 text-white" />
        </div>
      </div>
      <div>
        <h1 className="text-2xl font-bold text-gray-800">EVADE</h1>
        <p className="text-xs text-gray-500 -mt-1">
          Your trusted safety companion
        </p>
      </div>
    </div>
  );

  const ModeToggle = () => (
    <div className="bg-white/80 border border-gray-200/60 rounded-full p-1 shadow-sm">
      <div className="flex relative">
        <button
          onClick={() => setIsAdultMode(true)}
          className={`px-4 py-2 rounded-full text-sm font-medium transition-all flex items-center space-x-2 ${
            isAdultMode
              ? "bg-blue-500 text-white shadow-sm"
              : "text-gray-600 hover:text-gray-800 hover:bg-gray-50"
          }`}
        >
          <Shield className="w-4 h-4" />
          <span>Adult</span>
        </button>
        <button
          onClick={() => setIsAdultMode(false)}
          className={`px-4 py-2 rounded-full text-sm font-medium transition-all flex items-center space-x-2 ${
            !isAdultMode
              ? "bg-emerald-500 text-white shadow-sm"
              : "text-gray-600 hover:text-gray-800 hover:bg-gray-50"
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
      <div className="bg-white/70 border border-gray-200/50 rounded-3xl shadow-sm p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-800">
            EVADE Device Status
          </h2>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm font-medium text-green-700">
              Connected
            </span>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div className="bg-blue-50/50 rounded-xl p-4 text-center">
            <Battery className="w-6 h-6 text-blue-600 mx-auto mb-2" />
            <div className="text-sm font-medium text-gray-700">Battery</div>
            <div className="text-lg font-bold text-blue-600">87%</div>
          </div>
          <div className="bg-green-50/50 rounded-xl p-4 text-center">
            <Wifi className="w-6 h-6 text-green-600 mx-auto mb-2" />
            <div className="text-sm font-medium text-gray-700">Connection</div>
            <div className="text-sm font-bold text-green-600">Strong</div>
          </div>
          <div className="bg-purple-50/50 rounded-xl p-4 text-center">
            <Camera className="w-6 h-6 text-purple-600 mx-auto mb-2" />
            <div className="text-sm font-medium text-gray-700">Mode</div>
            <div className="text-sm font-bold text-purple-600">
              {isAdultMode ? "Adult" : "Kid"}
            </div>
          </div>
        </div>
      </div>

      {/* Safety Zone Status */}
      <div className="bg-green-50/70 border border-green-200/60 rounded-3xl shadow-sm p-6">
        <div className="flex items-center justify-center space-x-3">
          <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
            <MapPin className="w-6 h-6 text-green-600" />
          </div>
          <div className="text-center">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <h3 className="text-lg font-semibold text-green-800">
                You're in a Safe Zone
              </h3>
            </div>
            <p className="text-sm text-green-600 mt-1">
              Currently at Home - monitored and secure
            </p>
          </div>
        </div>
      </div>

      {/* Auto-Call Police Section - Only for Adult Mode */}
      {isAdultMode && (
        <div className="bg-white/70 border border-gray-200/50 rounded-3xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-800">Emergency Response</h3>
            <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
              Adult Mode
            </span>
          </div>
          <div className="bg-red-50/50 border border-red-200/30 rounded-xl p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <Phone className="w-5 h-5 text-red-600" />
                <div>
                  <span className="text-gray-700 font-medium">
                    Auto-Call Police
                  </span>
                  <p className="text-sm text-gray-600 mt-1">
                    Automatically contact authorities when high-risk offender
                    detected
                  </p>
                </div>
              </div>
              <button
                onClick={() =>
                  setAlertSettings({
                    ...alertSettings,
                    autoCallPolice: !alertSettings.autoCallPolice,
                  })
                }
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  alertSettings.autoCallPolice ? "bg-red-600" : "bg-gray-200"
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    alertSettings.autoCallPolice
                      ? "translate-x-6"
                      : "translate-x-1"
                  }`}
                />
              </button>
            </div>
            {alertSettings.autoCallPolice && (
              <div className="mt-4 p-3 bg-red-100/50 rounded-lg">
                <div className="flex items-start space-x-2">
                  <Shield className="w-4 h-4 text-red-600 mt-0.5" />
                  <div className="text-sm text-red-700">
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
      <div className="bg-white/70 border border-gray-200/50 rounded-3xl shadow-sm p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-800">
            Recent Activity
          </h3>
          <button
            onClick={() => setActiveTab("history")}
            className="text-blue-600 text-sm font-medium hover:text-blue-700"
          >
            View All
          </button>
        </div>

        <div className="space-y-3">
          {detectionHistory.slice(0, 2).map((detection) => (
            <div
              key={detection.id}
              className="flex items-center space-x-3 p-3 bg-red-50/50 rounded-xl"
            >
              <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center text-sm">
                {detection.photo}
              </div>
              <div className="flex-1">
                <div className="font-medium text-gray-800">
                  {detection.name}
                </div>
                <div className="text-sm text-gray-600">
                  {detection.riskLevel} Risk • {detection.timestamp}
                </div>
              </div>
              <div
                className={`px-2 py-1 rounded-full text-xs font-medium ${
                  detection.riskLevel === "High"
                    ? "bg-red-100 text-red-700"
                    : "bg-yellow-100 text-yellow-700"
                }`}
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
        <div className="inline-flex items-center space-x-2 bg-red-50/60 border border-red-200/50 rounded-full px-4 py-2 mb-4 shadow-sm">
          <History className="w-4 h-4 text-red-600" />
          <span className="text-sm font-medium text-red-700">
            Detection Log
          </span>
        </div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          Recent Detections
        </h2>
        <p className="text-gray-600">Offenders detected by your EVADE system</p>
      </div>

      <div className="space-y-4">
        {detectionHistory.map((detection) => (
          <div
            key={detection.id}
            className="bg-white/70 border border-gray-200/50 rounded-2xl shadow-sm p-6"
          >
            <div className="flex items-start space-x-4">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center text-2xl">
                {detection.photo}
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-bold text-gray-800">{detection.name}</h3>
                  <div
                    className={`px-3 py-1 rounded-full text-xs font-medium ${
                      detection.riskLevel === "High"
                        ? "bg-red-100 text-red-700"
                        : "bg-yellow-100 text-yellow-700"
                    }`}
                  >
                    {detection.riskLevel} Risk
                  </div>
                </div>
                <div className="space-y-1 mb-3">
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-gray-600">
                      Tier:
                    </span>
                    <span className="text-sm text-gray-800">
                      {detection.tier}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-gray-600">
                      Conviction:
                    </span>
                    <span className="text-sm text-gray-800">
                      {detection.conviction}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <MapPin className="w-4 h-4 text-gray-500" />
                    <span className="text-sm text-gray-600">
                      {detection.location}
                    </span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-500">
                    {detection.timestamp}
                  </span>
                  <button className="text-blue-600 text-sm font-medium hover:text-blue-700">
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
        <div className="inline-flex items-center space-x-2 bg-blue-50/60 border border-blue-200/50 rounded-full px-4 py-2 mb-4 shadow-sm">
          <Bell className="w-4 h-4 text-blue-600" />
          <span className="text-sm font-medium text-blue-700">
            {isAdultMode ? "Alert Settings" : "Alerts & Contacts"}
          </span>
        </div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          {isAdultMode ? "Notification Preferences" : "Safety Settings"}
        </h2>
        <p className="text-gray-600">
          {isAdultMode
            ? "Customize how you receive safety alerts"
            : "Manage alerts and emergency contacts"}
        </p>
      </div>

      {/* Alert Settings Section */}
      <div className="space-y-4">
        <div className="bg-white/70 border border-gray-200/50 rounded-2xl shadow-sm p-6">
          <h3 className="font-semibold text-gray-800 mb-4">
            Detection Sensitivity
          </h3>
          <div className="space-y-3">
            {["Low", "Medium", "High"].map((level) => (
              <label key={level} className="flex items-center space-x-3">
                <input
                  type="radio"
                  name="sensitivity"
                  checked={alertSettings.sensitivity === level}
                  onChange={() =>
                    setAlertSettings({ ...alertSettings, sensitivity: level })
                  }
                  className="w-4 h-4 text-blue-600"
                />
                <span className="text-gray-700">{level}</span>
              </label>
            ))}
          </div>
        </div>

        <div className="bg-white/70 border border-gray-200/50 rounded-2xl shadow-sm p-6">
          <h3 className="font-semibold text-gray-800 mb-4">
            Notification Types
          </h3>
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
                  <Icon className="w-5 h-5 text-gray-500" />
                  <span className="text-gray-700">{label}</span>
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
                      ? "bg-blue-600"
                      : "bg-gray-200"
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
          <div className="bg-white/70 border border-gray-200/50 rounded-2xl shadow-sm p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-semibold text-gray-800">
                Emergency Contacts
              </h3>
              <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                Kid Mode
              </span>
            </div>

            <div className="space-y-4 mb-6">
              {emergencyContacts.map((contact) => (
                <div
                  key={contact.id}
                  className="bg-purple-50/50 border border-purple-200/30 rounded-xl p-4"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div
                        className={`w-10 h-10 rounded-full flex items-center justify-center ${
                          contact.primary
                            ? "bg-purple-100 text-purple-600"
                            : "bg-gray-100 text-gray-600"
                        }`}
                      >
                        <Users className="w-5 h-5" />
                      </div>
                      <div>
                        <div className="flex items-center space-x-2">
                          <h4 className="font-medium text-gray-800">
                            {contact.name}
                          </h4>
                          {contact.primary && (
                            <span className="bg-purple-100 text-purple-700 text-xs px-2 py-1 rounded-full">
                              Primary
                            </span>
                          )}
                        </div>
                        <p className="text-sm text-gray-600">{contact.phone}</p>
                        <p className="text-xs text-gray-500">
                          {contact.relation}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-1">
                      <button className="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all">
                        <Edit className="w-3.5 h-3.5" />
                      </button>
                      <button className="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all">
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <button className="w-full bg-purple-50 border-2 border-dashed border-purple-200 rounded-xl p-4 text-purple-600 hover:bg-purple-100 transition-all">
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
    <div className="min-h-screen bg-gradient-to-br from-blue-50/30 via-white to-emerald-50/30 flex flex-col">
      {/* Subtle background pattern */}
      <div className="absolute inset-0 opacity-30">
        <div
          className="absolute inset-0"
          style={{
            backgroundImage:
              "radial-gradient(circle at 1px 1px, rgba(59, 130, 246, 0.1) 1px, transparent 0)",
            backgroundSize: "20px 20px",
          }}
        ></div>
      </div>

      {/* Header */}
      <header className="relative bg-white/60 border-b border-gray-200/40 shadow-sm backdrop-blur-sm">
        <div className="max-w-6xl mx-auto flex items-center justify-between p-6">
          <LogoComponent />
          <ModeToggle />
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 flex-1 max-w-4xl mx-auto w-full p-6 py-12 pb-24">
        {renderContent()}
      </main>

      {/* Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 bg-white/60 border-t border-gray-200/40 shadow-sm backdrop-blur-sm z-50">
        <div className="max-w-6xl mx-auto px-6">
          <div className="flex justify-around py-4">
            {[
              { id: "home", icon: Home, label: "Dashboard" },
              { id: "history", icon: History, label: "Detections" },
              { id: "alerts", icon: Bell, label: "Alerts" },
            ].map(({ id, icon: Icon, label }) => (
              <button
                key={id}
                onClick={() => setActiveTab(id)}
                className={`flex flex-col items-center space-y-2 px-8 py-3 rounded-xl transition-all ${
                  activeTab === id
                    ? "bg-white/80 shadow-sm border border-gray-200/50"
                    : "hover:bg-white/40"
                }`}
              >
                <Icon
                  className={`w-5 h-5 ${
                    activeTab === id ? "text-gray-700" : "text-gray-500"
                  }`}
                />
                <span
                  className={`text-xs font-medium ${
                    activeTab === id ? "text-gray-700" : "text-gray-500"
                  }`}
                >
                  {label}
                </span>
              </button>
            ))}
          </div>
        </div>
      </nav>
    </div>
  );
};

export default App;
