import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Eye, EyeOff, Mail, Lock, User, BookOpen, GraduationCap, Users, Shield, Sparkles, ArrowRight, CheckCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const SignupForm = ({ onToggleForm }) => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    userType: 'student'
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [toggleLoading, setToggleLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const userTypes = [
    {
      value: 'student',
      label: 'Student',
      icon: GraduationCap,
      description: 'Learn and enroll in courses',
      color: 'blue'
    },
    {
      value: 'instructor',
      label: 'Instructor',
      icon: Users,
      description: 'Create and manage courses',
      color: 'purple'
    },
    {
      value: 'admin',
      label: 'Admin',
      icon: Shield,
      description: 'Manage the platform',
      color: 'orange'
    }
  ];

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Signup form submitted with data:', formData); // Debug log
    
    // Basic validation
    if (!formData.username || !formData.email || !formData.password || !formData.confirmPassword || !formData.userType) {
      console.log('Validation failed: missing required fields');
      return;
    }
    
    if (formData.password !== formData.confirmPassword) {
      console.log('Validation failed: passwords do not match');
      return;
    }
    
    if (formData.password.length < 8) {
      console.log('Validation failed: password too short');
      return;
    }
    
    setLoading(true);
    
    try {
      // Convert userType to user_type for backend compatibility
      const backendData = {
        username: formData.username,
        email: formData.email,
        password: formData.password,
        user_type: formData.userType // Convert to snake_case for backend
      };
      
      console.log('Sending data to backend:', backendData);
      
      const result = await register(backendData);
      console.log('Signup result:', result);
      
      if (result.success) {
        console.log('Signup successful, navigating to dashboard for user type:', result.userType);
        switch (result.userType) {
          case 'student':
            navigate('/student-home');
            break;
          case 'instructor':
            navigate('/instructor-home');
            break;
          case 'admin':
            navigate('/admin-home');
            break;
          default:
            console.log('Unknown user type, navigating to home');
            navigate('/');
        }
      } else {
        console.log('Signup failed:', result.error);
      }
    } catch (error) {
      console.error('Signup error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getColorClasses = (color) => {
    const colors = {
      blue: 'border-blue-200 bg-blue-50 text-blue-900',
      purple: 'border-purple-200 bg-purple-50 text-purple-900',
      orange: 'border-orange-200 bg-orange-50 text-orange-900'
    };
    return colors[color] || colors.blue;
  };

  const getIconColor = (color) => {
    const colors = {
      blue: 'text-blue-600',
      purple: 'text-purple-600',
      orange: 'text-orange-600'
    };
    return colors[color] || colors.blue;
  };

  return (
    <div className="w-full max-w-md mx-auto animate-fade-in">
      {/* Header Section */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-green-500 to-blue-600 rounded-2xl mb-6 shadow-lg">
          <BookOpen className="w-10 h-10" />
        </div>
        <h2 className="text-4xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text mb-3">
          Join Us
        </h2>
        <p className="text-gray-600 text-lg">Create your account to start your learning journey</p>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="form-group">
          <label htmlFor="username" className="form-label">
            Username
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <User className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              className="form-input pl-12"
              placeholder="Choose a username"
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="email" className="form-label">
            Email
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <Mail className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="form-input pl-12"
              placeholder="Enter your email"
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">Account Type</label>
          <div className="grid grid-cols-1 gap-3">
            {userTypes.map((type) => {
              const Icon = type.icon;
              const isSelected = formData.userType === type.value;
              return (
                <label
                  key={type.value}
                  className={`relative flex items-center p-4 border-2 rounded-xl cursor-pointer transition-all duration-200 hover:shadow-md ${
                    isSelected
                      ? `${getColorClasses(type.color)} border-current shadow-lg`
                      : 'border-gray-200 hover:border-gray-300 bg-white'
                  }`}
                >
                  <input
                    type="radio"
                    name="userType"
                    value={type.value}
                    checked={isSelected}
                    onChange={handleChange}
                    className="sr-only"
                  />
                  <div className="flex items-center space-x-4">
                    <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                      isSelected ? 'bg-white' : 'bg-gray-100'
                    }`}>
                      <Icon className={`h-6 w-6 ${isSelected ? getIconColor(type.color) : 'text-gray-400'}`} />
                    </div>
                    <div className="flex-1">
                      <div className={`font-semibold text-lg ${
                        isSelected ? 'text-current' : 'text-gray-900'
                      }`}>
                        {type.label}
                      </div>
                      <div className={`text-sm ${
                        isSelected ? 'text-current opacity-80' : 'text-gray-500'
                      }`}>
                        {type.description}
                      </div>
                    </div>
                    {isSelected && (
                      <CheckCircle className={`h-6 w-6 ${getIconColor(type.color)}`} />
                    )}
                  </div>
                </label>
              );
            })}
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="password" className="form-label">
            Password
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <Lock className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type={showPassword ? 'text' : 'password'}
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="form-input pl-12 pr-12"
              placeholder="Create a password"
              required
            />
            <button
              type="button"
              className="absolute inset-y-0 right-0 pr-4 flex items-center hover:text-gray-600 transition-colors"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? (
                <EyeOff className="h-5 w-5 text-gray-400" />
              ) : (
                <Eye className="h-5 w-5 text-gray-400" />
              )}
            </button>
          </div>
          <div className="mt-2 text-xs text-gray-500">
            Password must be at least 8 characters long
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="confirmPassword" className="form-label">
            Confirm Password
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <Lock className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type={showConfirmPassword ? 'text' : 'password'}
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              className="form-input pl-12 pr-12"
              placeholder="Confirm your password"
              required
            />
            <button
              type="button"
              className="absolute inset-y-0 right-0 pr-4 flex items-center hover:text-gray-600 transition-colors"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            >
              {showConfirmPassword ? (
                <EyeOff className="h-5 w-5 text-gray-400" />
              ) : (
                <Eye className="h-5 w-5 text-gray-400" />
              )}
            </button>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="btn btn-primary btn-full btn-lg"
          onClick={() => console.log('Signup button clicked!')}
        >
          {loading ? (
            <div className="flex items-center justify-center">
              <div className="loading-spinner mr-3"></div>
              Creating Account...
            </div>
          ) : (
            <>
              Create Account
              <ArrowRight className="w-5 h-5 ml-2" />
            </>
          )}
        </button>
      </form>

      {/* Toggle Form */}
      <div className="mt-8 text-center">
        <p className="text-gray-600">
          Already have an account?{' '}
          <button
            onClick={() => {
              console.log('Sign in here button clicked!');
              setToggleLoading(true);
              setTimeout(() => {
                onToggleForm();
                setToggleLoading(false);
              }, 100);
            }}
            disabled={toggleLoading}
            className="auth-toggle-button"
          >
            {toggleLoading ? 'Loading...' : 'Sign in here'}
          </button>
        </p>
      </div>

      {/* Benefits */}
      <div className="mt-8 p-6 bg-gradient-to-br from-green-50 to-blue-50 rounded-2xl border border-green-100">
        <div className="flex items-center mb-4">
          <Sparkles className="w-5 h-5 text-green-600 mr-2" />
          <h4 className="font-semibold text-green-900">Why Join Us?</h4>
        </div>
        <div className="space-y-3">
          <div className="flex items-center text-sm">
            <CheckCircle className="w-4 h-4 text-green-600 mr-3 flex-shrink-0" />
            <span className="text-green-800">Access to premium courses and content</span>
          </div>
          <div className="flex items-center text-sm">
            <CheckCircle className="w-4 h-4 text-green-600 mr-3 flex-shrink-0" />
            <span className="text-green-800">Learn at your own pace</span>
          </div>
          <div className="flex items-center text-sm">
            <CheckCircle className="w-4 h-4 text-green-600 mr-3 flex-shrink-0" />
            <span className="text-green-800">Get certificates upon completion</span>
          </div>
          <div className="flex items-center text-sm">
            <CheckCircle className="w-4 h-4 text-green-600 mr-3 flex-shrink-0" />
            <span className="text-green-800">Join a community of learners</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignupForm; 