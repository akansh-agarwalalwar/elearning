import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import LoginForm from './components/LoginForm';
import SignupForm from './components/SignupForm';
import StudentDashboard from './pages/StudentDashboard';
import InstructorDashboard from './pages/InstructorDashboard';
import AdminDashboard from './pages/AdminDashboard';

function AuthGate({ children, role }) {
  const { isAuthenticated, user, loading } = useAuth();
  
  console.log('AuthGate - loading:', loading, 'isAuthenticated:', isAuthenticated(), 'user:', user, 'required role:', role); // Debug log
  
  if (loading) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  if (!isAuthenticated()) {
    console.log('AuthGate - redirecting to login'); // Debug log
    return <Navigate to="/login" />;
  }
  if (role && user?.userType !== role) {
    console.log('AuthGate - role mismatch, redirecting to correct dashboard'); // Debug log
    return <Navigate to={`/${user?.userType}-home`} />;
  }
  return children;
}

function HomeRedirect() {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" />;
  if (user.userType === 'student') return <Navigate to="/student-home" />;
  if (user.userType === 'instructor') return <Navigate to="/instructor-home" />;
  if (user.userType === 'admin') return <Navigate to="/admin-home" />;
  return <Navigate to="/login" />;
}

function AuthPages() {
  const [showSignup, setShowSignup] = useState(false);
  
  const handleToggleToSignup = () => {
    console.log('Toggle to signup clicked, current state:', showSignup);
    setShowSignup(true);
    console.log('Set showSignup to true');
  };
  
  const handleToggleToLogin = () => {
    console.log('Toggle to login clicked, current state:', showSignup);
    setShowSignup(false);
    console.log('Set showSignup to false');
  };
  
  console.log('AuthPages rendering, showSignup:', showSignup);
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50 px-4 py-8 relative">
      <div className="w-full max-w-lg relative z-10">
        <div className="bg-white rounded-3xl shadow-2xl p-8 animate-slide-up border border-gray-100">
          {showSignup ? (
            <SignupForm onToggleForm={handleToggleToLogin} />
          ) : (
            <LoginForm onToggleForm={handleToggleToSignup} />
          )}
        </div>
        
        {/* Background decoration */}
        <div className="absolute inset-0 -z-10 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-400 to-purple-600 rounded-full opacity-10 blur-3xl"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-purple-400 to-pink-600 rounded-full opacity-10 blur-3xl"></div>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <Toaster position="top-center" />
        <Routes>
          <Route path="/" element={<HomeRedirect />} />
          <Route path="/login" element={<AuthPages />} />
          <Route path="/signup" element={<AuthPages />} />
          <Route
            path="/student-home"
            element={
              <AuthGate role="student">
                <StudentDashboard />
              </AuthGate>
            }
          />
          <Route
            path="/instructor-home"
            element={
              <AuthGate role="instructor">
                <InstructorDashboard />
              </AuthGate>
            }
          />
          <Route
            path="/admin-home"
            element={
              <AuthGate role="admin">
                <AdminDashboard />
              </AuthGate>
            }
          />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;