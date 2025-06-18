import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { 
  BarChart3, BookOpen, Users, DollarSign, TrendingUp, TrendingDown,
  Search, Filter, Download, Plus, Edit3, Eye, MoreHorizontal,
  Calendar, Clock, Star, Award, Target, Activity, Bell, Settings,
  User, LogOut, ChevronDown, ChevronRight, Play, Pause, CheckCircle2,
  AlertTriangle, MessageSquare, PieChart, LineChart, ArrowUpRight,
  ArrowDownRight, Zap, Globe, Mail, Phone, FileText, Image, Video,
  Sparkles, Crown, Trophy, Rocket, Lightbulb, Brain, Code, Palette
} from 'lucide-react';

const ProfessionalInstructorDashboard = () => {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTimeRange, setSelectedTimeRange] = useState('7d');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const mockUser = { 
    name: user?.username,
    email: user?.email,
    avatar: 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150',
    role: 'Senior Instructor',
    joinDate: '2019'
  };

  useEffect(() => {
    setTimeout(() => {
      const mockCourses = [
        {
          id: 1,
          title: 'Advanced Data Science with Python',
          status: 'published',
          students: 2847,
          rating: 4.9,
          revenue: 89250,
          progress: 95,
          lastUpdated: '2024-02-18',
          category: 'Data Science',
          thumbnail: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=300',
          completionRate: 87,
          totalLessons: 42,
          completedLessons: 40,
          duration: '24h 30m',
          reviews: 394
        },
        {
          id: 2,
          title: 'Machine Learning Fundamentals',
          status: 'published',
          students: 1956,
          rating: 4.8,
          revenue: 67830,
          progress: 100,
          lastUpdated: '2024-02-15',
          category: 'Machine Learning',
          thumbnail: 'https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=300',
          completionRate: 91,
          totalLessons: 35,
          completedLessons: 35,
          duration: '18h 45m',
          reviews: 287
        },
        {
          id: 3,
          title: 'Deep Learning Neural Networks',
          status: 'draft',
          students: 0,
          rating: 0,
          revenue: 0,
          progress: 65,
          lastUpdated: '2024-02-20',
          category: 'Deep Learning',
          thumbnail: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=300',
          completionRate: 0,
          totalLessons: 48,
          completedLessons: 31,
          duration: '32h 15m',
          reviews: 0
        },
        {
          id: 4,
          title: 'Statistical Analysis & Visualization',
          status: 'published',
          students: 3241,
          rating: 4.7,
          revenue: 94570,
          progress: 100,
          lastUpdated: '2024-02-12',
          category: 'Statistics',
          thumbnail: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=300',
          completionRate: 89,
          totalLessons: 28,
          completedLessons: 28,
          duration: '16h 20m',
          reviews: 456
        }
      ];
      setCourses(mockCourses);
      setLoading(false);
    }, 800);
  }, []);

  const stats = {
    totalRevenue: courses.reduce((sum, course) => sum + course.revenue, 0),
    totalStudents: courses.reduce((sum, course) => sum + course.students, 0),
    totalCourses: courses.length,
    avgRating: courses.length ? (courses.reduce((sum, course) => sum + course.rating, 0) / courses.filter(c => c.rating > 0).length).toFixed(1) : '0.0',
    publishedCourses: courses.filter(c => c.status === 'published').length,
    completionRate: courses.length ? (courses.reduce((sum, course) => sum + course.completionRate, 0) / courses.filter(c => c.completionRate > 0).length).toFixed(1) : '0.0'
  };

  const revenueChange = '+12.5%';
  const studentsChange = '+8.3%';
  const ratingChange = '+0.2%';
  const completionChange = '+5.1%';

  const sidebarItems = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3, color: 'from-blue-600 to-purple-600' },
    { id: 'courses', label: 'My Courses', icon: BookOpen, color: 'from-emerald-600 to-teal-600' },
    { id: 'students', label: 'Students', icon: Users, color: 'from-orange-600 to-red-600' },
    { id: 'analytics', label: 'Analytics', icon: TrendingUp, color: 'from-purple-600 to-pink-600' },
    { id: 'messages', label: 'Messages', icon: MessageSquare, color: 'from-indigo-600 to-blue-600' },
    { id: 'settings', label: 'Settings', icon: Settings, color: 'from-gray-600 to-slate-600' }
  ];

  const StatusBadge = ({ status }) => {
    const config = {
      published: { color: 'bg-emerald-100 text-emerald-700 border-emerald-200', icon: CheckCircle2 },
      draft: { color: 'bg-amber-100 text-amber-700 border-amber-200', icon: Edit3 },
      archived: { color: 'bg-slate-100 text-slate-700 border-slate-200', icon: Pause }
    };
    
    const { color, icon: Icon } = config[status] || config.draft;
    
    return (
      <span className={`inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium border ${color}`}>
        <Icon className="w-3 h-3 mr-1" />
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    );
  };

  const MetricCard = ({ title, value, change, icon: Icon, trend = 'up', gradient = 'from-blue-600 to-purple-600' }) => (
    <div className="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg transition-all duration-300 group">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className={`p-3 bg-gradient-to-br ${gradient} rounded-xl group-hover:scale-110 transition-transform duration-300`}>
            <Icon className="w-6 h-6 text-white" />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-600">{title}</p>
            <p className="text-2xl font-bold text-slate-900 mt-1">{value}</p>
          </div>
        </div>
        <div className={`flex items-center space-x-1 text-sm font-medium ${
          trend === 'up' ? 'text-emerald-600' : 'text-red-600'
        }`}>
          {trend === 'up' ? (
            <ArrowUpRight className="w-4 h-4" />
          ) : (
            <ArrowDownRight className="w-4 h-4" />
          )}
          <span>{change}</span>
        </div>
      </div>
    </div>
  );

  const CourseCard = ({ course }) => (
    <div className="bg-white rounded-xl border border-slate-200 p-6 hover:shadow-lg transition-all duration-300 group">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-start space-x-4">
          <div className="w-16 h-16 bg-gradient-to-br from-blue-100 to-purple-100 rounded-lg overflow-hidden group-hover:scale-105 transition-transform duration-300">
            <img 
              src={course.thumbnail} 
              alt={course.title}
              className="w-full h-full object-cover"
            />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-slate-900 mb-1 group-hover:text-blue-600 transition-colors">
              {course.title}
            </h3>
            <p className="text-sm text-slate-500 mb-2">{course.category}</p>
            <StatusBadge status={course.status} />
          </div>
        </div>
        <button className="p-1 hover:bg-slate-100 rounded-lg transition-colors">
          <MoreHorizontal className="w-4 h-4 text-slate-400" />
        </button>
      </div>

      <div className="grid grid-cols-3 gap-4 mb-4">
        <div className="text-center">
          <p className="text-lg font-bold text-slate-900">{course.students.toLocaleString()}</p>
          <p className="text-xs text-slate-500">Students</p>
        </div>
        <div className="text-center">
          <p className="text-lg font-bold text-slate-900 flex items-center justify-center">
            <Star className="w-4 h-4 text-yellow-500 mr-1" />
            {course.rating || 'N/A'}
          </p>
          <p className="text-xs text-slate-500">Rating</p>
        </div>
        <div className="text-center">
          <p className="text-lg font-bold text-emerald-600">${course.revenue.toLocaleString()}</p>
          <p className="text-xs text-slate-500">Revenue</p>
        </div>
      </div>

      {course.status !== 'draft' && (
        <div className="mb-4">
          <div className="flex justify-between text-sm text-slate-600 mb-1">
            <span>Completion Rate</span>
            <span>{course.completionRate}%</span>
          </div>
          <div className="w-full bg-slate-200 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-blue-600 to-purple-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${course.completionRate}%` }}
            />
          </div>
        </div>
      )}

      <div className="flex items-center justify-between text-sm text-slate-500 mb-4">
        <span>{course.completedLessons}/{course.totalLessons} lessons</span>
        <span>{course.duration}</span>
        <span>Updated {new Date(course.lastUpdated).toLocaleDateString()}</span>
      </div>

      <div className="flex space-x-2">
        <button className="flex-1 bg-slate-100 hover:bg-slate-200 text-slate-700 py-2 px-4 rounded-lg font-medium transition-colors flex items-center justify-center">
          <Eye className="w-4 h-4 mr-2" />
          View
        </button>
        <button className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-2 px-4 rounded-lg font-medium transition-all duration-200 flex items-center justify-center">
          <Edit3 className="w-4 h-4 mr-2" />
          Edit
        </button>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="relative">
            <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
            <div className="absolute inset-0 w-16 h-16 border-4 border-transparent border-t-purple-600 rounded-full animate-spin mx-auto" style={{ animationDelay: '0.5s' }}></div>
          </div>
          <p className="text-slate-600 font-medium text-lg">Loading your dashboard...</p>
          <p className="text-slate-400 text-sm mt-2">Preparing your course analytics</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex w-full">
      {/* Sidebar */}
      <div className={`bg-white/90 backdrop-blur-sm border-r border-slate-200/50 transition-all duration-300 flex-shrink-0 ${
        sidebarCollapsed ? 'w-16' : 'w-64'
      }`}>
        <div className="p-6">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center shadow-lg">
              <BookOpen className="w-5 h-5 text-white" />
            </div>
            {!sidebarCollapsed && (
              <span className="font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">EduLearn Pro</span>
            )}
          </div>
        </div>

        <nav className="mt-6">
          {sidebarItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center space-x-3 px-6 py-3 text-left transition-all duration-300 ${
                  activeTab === item.id
                    ? `bg-gradient-to-r ${item.color} text-white shadow-lg transform scale-105`
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900 hover:scale-105'
                }`}
              >
                <Icon className="w-5 h-5" />
                {!sidebarCollapsed && <span className="font-medium">{item.label}</span>}
              </button>
            );
          })}
        </nav>

        <div className="absolute bottom-6 left-6 right-6">
          {!sidebarCollapsed && (
            <div className="bg-gradient-to-r from-slate-50 to-blue-50 rounded-lg p-4 border border-slate-200/50">
              <div className="flex items-center space-x-3">
                <img 
                  src={mockUser.avatar} 
                  alt={mockUser.name}
                  className="w-10 h-10 rounded-full border-2 border-white shadow-md"
                />
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-slate-900 truncate">{mockUser.name}</p>
                  <p className="text-sm text-slate-500 truncate">{mockUser.role}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="bg-white/90 backdrop-blur-sm border-b border-slate-200/50 px-6 py-4 flex-shrink-0">
          <div className="flex items-center justify-between w-full">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
                className="p-2 hover:bg-slate-100 rounded-lg transition-colors group"
              >
                <ChevronRight className={`w-5 h-5 transition-transform group-hover:scale-110 ${!sidebarCollapsed ? 'rotate-180' : ''}`} />
              </button>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-900 to-slate-600 bg-clip-text text-transparent">
                  {sidebarItems.find(item => item.id === activeTab)?.label}
                </h1>
                <p className="text-slate-500">
                  {activeTab === 'dashboard' && 'Overview of your teaching performance'}
                  {activeTab === 'courses' && 'Manage and track your courses'}
                  {activeTab === 'students' && 'Monitor student progress and engagement'}
                  {activeTab === 'analytics' && 'Detailed insights and reports'}
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <button className="relative p-2 hover:bg-slate-100 rounded-lg transition-colors group">
                <Bell className="w-5 h-5 text-slate-600 group-hover:scale-110 transition-transform" />
                <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full animate-pulse"></span>
              </button>
              <button className="p-2 hover:bg-slate-100 rounded-lg transition-colors group">
                <Settings className="w-5 h-5 text-slate-600 group-hover:scale-110 transition-transform" />
              </button>
              <button 
                onClick={logout}
                className="p-2 hover:bg-red-50 hover:text-red-600 rounded-lg transition-colors group"
                title="Logout"
              >
                <LogOut className="w-5 h-5 group-hover:scale-110 transition-transform" />
              </button>
            </div>
          </div>
        </header>

        {/* Content */}
        <main className="flex-1 p-6 overflow-auto">
          {activeTab === 'dashboard' && (
            <div className="space-y-6 w-full">
              {/* Welcome Banner */}
              <div className="bg-gradient-to-r from-slate-900 via-blue-900 to-purple-900 rounded-2xl p-8 text-white shadow-2xl relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-purple-600/20"></div>
                <div className="relative z-10 flex items-center justify-between">
                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center">
                        <Sparkles className="h-6 w-6 text-white" />
                      </div>
                      <div>
                        <h1 className="text-3xl font-bold">
                          Welcome back, {user?.username}! 👨‍🏫
                        </h1>
                        <p className="text-blue-100 text-lg">Your courses are performing excellently this month</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-6 text-sm">
                      <div className="flex items-center space-x-2">
                        <TrendingUp className="h-4 w-4 text-emerald-400" />
                        <span className="text-emerald-400">+23% growth</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Users className="h-4 w-4 text-blue-400" />
                        <span className="text-blue-400">{stats.totalStudents.toLocaleString()} students</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Star className="h-4 w-4 text-yellow-400" />
                        <span className="text-yellow-400">{stats.avgRating} avg rating</span>
                      </div>
                    </div>
                  </div>
                  <div className="hidden lg:block">
                    <div className="w-24 h-24 bg-white/10 backdrop-blur-sm rounded-2xl flex items-center justify-center border border-white/20">
                      <Trophy className="h-12 w-12 text-yellow-400" />
                    </div>
                  </div>
                </div>
              </div>

              {/* Metrics */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricCard
                  title="Total Revenue"
                  value={`$${stats.totalRevenue.toLocaleString()}`}
                  change={revenueChange}
                  icon={DollarSign}
                  gradient="from-emerald-600 to-teal-600"
                />
                <MetricCard
                  title="Active Students"
                  value={stats.totalStudents.toLocaleString()}
                  change={studentsChange}
                  icon={Users}
                  gradient="from-blue-600 to-purple-600"
                />
                <MetricCard
                  title="Course Rating"
                  value={stats.avgRating}
                  change={ratingChange}
                  icon={Star}
                  gradient="from-yellow-600 to-orange-600"
                />
                <MetricCard
                  title="Completion Rate"
                  value={`${stats.completionRate}%`}
                  change={completionChange}
                  icon={Target}
                  gradient="from-purple-600 to-pink-600"
                />
              </div>

              {/* Charts Section */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white/90 backdrop-blur-sm rounded-2xl border border-slate-200/50 p-6 shadow-lg">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="font-semibold text-slate-900">Revenue Analytics</h3>
                    <select 
                      value={selectedTimeRange}
                      onChange={(e) => setSelectedTimeRange(e.target.value)}
                      className="text-sm border border-slate-300 rounded-lg px-3 py-1 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="7d">Last 7 days</option>
                      <option value="30d">Last 30 days</option>
                      <option value="90d">Last 3 months</option>
                    </select>
                  </div>
                  <div className="h-64 flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl">
                    <div className="text-center">
                      <BarChart3 className="w-12 h-12 text-blue-600 mx-auto mb-4" />
                      <p className="text-slate-600">Revenue chart visualization would go here</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white/90 backdrop-blur-sm rounded-2xl border border-slate-200/50 p-6 shadow-lg">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="font-semibold text-slate-900">Student Engagement</h3>
                    <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                      View Details
                    </button>
                  </div>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl">
                      <div className="flex items-center space-x-3">
                        <div className="w-3 h-3 bg-blue-600 rounded-full"></div>
                        <span className="text-sm font-medium text-slate-900">Active This Week</span>
                      </div>
                      <span className="text-lg font-bold text-blue-600">2,847</span>
                    </div>
                    <div className="flex items-center justify-between p-4 bg-gradient-to-r from-emerald-50 to-teal-50 rounded-xl">
                      <div className="flex items-center space-x-3">
                        <div className="w-3 h-3 bg-emerald-600 rounded-full"></div>
                        <span className="text-sm font-medium text-slate-900">Completed Courses</span>
                      </div>
                      <span className="text-lg font-bold text-emerald-600">1,234</span>
                    </div>
                    <div className="flex items-center justify-between p-4 bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl">
                      <div className="flex items-center space-x-3">
                        <div className="w-3 h-3 bg-amber-600 rounded-full"></div>
                        <span className="text-sm font-medium text-slate-900">In Progress</span>
                      </div>
                      <span className="text-lg font-bold text-amber-600">1,613</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Recent Activity */}
              <div className="bg-white/90 backdrop-blur-sm rounded-2xl border border-slate-200/50 p-6 shadow-lg">
                <h3 className="font-semibold text-slate-900 mb-6">Recent Activity</h3>
                <div className="space-y-4">
                  {[
                    { type: 'enrollment', message: '23 new students enrolled in "Advanced Data Science"', time: '2 hours ago', color: 'bg-blue-100 text-blue-600', icon: Users },
                    { type: 'review', message: 'New 5-star review received for "Machine Learning Fundamentals"', time: '4 hours ago', color: 'bg-yellow-100 text-yellow-600', icon: Star },
                    { type: 'completion', message: '12 students completed "Statistical Analysis" course', time: '6 hours ago', color: 'bg-emerald-100 text-emerald-600', icon: CheckCircle2 },
                    { type: 'revenue', message: 'Revenue milestone: $100k total earnings reached', time: '1 day ago', color: 'bg-purple-100 text-purple-600', icon: DollarSign }
                  ].map((activity, index) => {
                    const Icon = activity.icon;
                    return (
                      <div key={index} className="flex items-start space-x-4 p-4 hover:bg-slate-50 rounded-xl transition-colors group">
                        <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${activity.color} group-hover:scale-110 transition-transform`}>
                          <Icon className="w-5 h-5" />
                        </div>
                        <div className="flex-1">
                          <p className="text-sm text-slate-900 font-medium">{activity.message}</p>
                          <p className="text-xs text-slate-500 mt-1">{activity.time}</p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'courses' && (
            <div className="space-y-6 w-full">
              {/* Course Management Header */}
              <div className="bg-white/90 backdrop-blur-sm rounded-2xl border border-slate-200/50 p-6 shadow-lg">
                <div className="flex flex-col lg:flex-row gap-4">
                  <div className="flex-1 relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <input
                      type="text"
                      placeholder="Search courses..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="w-full pl-10 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div className="flex space-x-3">
                    <button className="bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-3 rounded-lg font-medium transition-colors flex items-center">
                      <Filter className="w-4 h-4 mr-2" />
                      Filter
                    </button>
                    <button className="bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-3 rounded-lg font-medium transition-colors flex items-center">
                      <Download className="w-4 h-4 mr-2" />
                      Export
                    </button>
                    <button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center shadow-lg">
                      <Plus className="w-4 h-4 mr-2" />
                      Create Course
                    </button>
                  </div>
                </div>
              </div>

              {/* Course Cards */}
              <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                {courses
                  .filter(course => 
                    course.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                    course.category.toLowerCase().includes(searchTerm.toLowerCase())
                  )
                  .map(course => (
                    <CourseCard key={course.id} course={course} />
                  ))
                }
              </div>
            </div>
          )}

          {activeTab === 'students' && (
            <div className="space-y-6 w-full">
              <div className="bg-white/90 backdrop-blur-sm rounded-2xl border border-slate-200/50 p-6 shadow-lg">
                <h3 className="font-semibold text-slate-900 mb-4">Student Overview</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="text-center p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl">
                    <p className="text-3xl font-bold text-blue-600 mb-2">{stats.totalStudents.toLocaleString()}</p>
                    <p className="text-sm text-slate-600">Total Enrolled</p>
                  </div>
                  <div className="text-center p-6 bg-gradient-to-r from-emerald-50 to-teal-50 rounded-xl">
                    <p className="text-3xl font-bold text-emerald-600 mb-2">2,847</p>
                    <p className="text-sm text-slate-600">Active This Month</p>
                  </div>
                  <div className="text-center p-6 bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl">
                    <p className="text-3xl font-bold text-amber-600 mb-2">{stats.completionRate}%</p>
                    <p className="text-sm text-slate-600">Avg Completion</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'analytics' && (
            <div className="space-y-6 w-full">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white/90 backdrop-blur-sm rounded-2xl border border-slate-200/50 p-6 shadow-lg">
                  <h3 className="font-semibold text-slate-900 mb-6">Performance Metrics</h3>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center p-4 bg-gradient-to-r from-emerald-50 to-teal-50 rounded-xl">
                      <span className="text-sm text-slate-600">Course Completion Rate</span>
                      <span className="text-lg font-bold text-emerald-600">{stats.completionRate}%</span>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-xl">
                      <span className="text-sm text-slate-600">Average Rating</span>
                      <span className="text-lg font-bold text-yellow-600">{stats.avgRating}/5.0</span>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl">
                      <span className="text-sm text-slate-600">Student Retention</span>
                      <span className="text-lg font-bold text-blue-600">94.2%</span>
                    </div>
                  </div>
                </div>

                <div className="bg-white/90 backdrop-blur-sm rounded-2xl border border-slate-200/50 p-6 shadow-lg">
                  <h3 className="font-semibold text-slate-900 mb-6">Revenue Breakdown</h3>
                  <div className="space-y-4">
                    {courses.filter(c => c.status === 'published').map(course => (
                      <div key={course.id} className="flex justify-between items-center p-3 border-l-4 border-blue-600 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
                        <span className="text-sm font-medium text-slate-900">{course.title}</span>
                        <span className="text-sm font-bold text-emerald-600">${course.revenue.toLocaleString()}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default ProfessionalInstructorDashboard;