import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { 
  BookOpen, 
  GraduationCap, 
  Search, 
  Filter, 
  Play, 
  Clock, 
  Users, 
  Star,
  LogOut,
  User,
  Bell,
  TrendingUp,
  Award,
  Calendar,
  Target
} from 'lucide-react';

const StudentDashboard = () => {
  const { user, logout } = useAuth();
  const [courses, setCourses] = useState([]);
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    // Simulate fetching courses
    setTimeout(() => {
      const mockCourses = [
        {
          id: 1,
          title: 'Advanced Python Programming',
          description: 'Master Python with advanced concepts and real-world projects',
          instructor: 'Dr. Sarah Johnson',
          duration: '8 weeks',
          students: 1247,
          rating: 4.8,
          price: '$99',
          image: 'https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=400',
          category: 'Programming',
          progress: 75
        },
        {
          id: 2,
          title: 'Web Development Fundamentals',
          description: 'Learn HTML, CSS, and JavaScript from scratch',
          instructor: 'Mike Chen',
          duration: '6 weeks',
          students: 2156,
          rating: 4.6,
          price: '$79',
          image: 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=400',
          category: 'Web Development'
        },
        {
          id: 3,
          title: 'Data Science Essentials',
          description: 'Introduction to data analysis and machine learning',
          instructor: 'Dr. Emily Rodriguez',
          duration: '10 weeks',
          students: 892,
          rating: 4.9,
          price: '$129',
          image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400',
          category: 'Data Science'
        },
        {
          id: 4,
          title: 'UI/UX Design Masterclass',
          description: 'Create beautiful and functional user interfaces',
          instructor: 'Alex Thompson',
          duration: '7 weeks',
          students: 1567,
          rating: 4.7,
          price: '$89',
          image: 'https://images.unsplash.com/photo-1561070791-2526d30994b5?w=400',
          category: 'Design'
        },
        {
          id: 5,
          title: 'Digital Marketing Strategy',
          description: 'Learn modern marketing techniques and strategies',
          instructor: 'Lisa Wang',
          duration: '5 weeks',
          students: 2341,
          rating: 4.5,
          price: '$69',
          image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400',
          category: 'Business'
        },
        {
          id: 6,
          title: 'Mobile App Development',
          description: 'Build iOS and Android apps with React Native',
          instructor: 'David Kim',
          duration: '9 weeks',
          students: 1123,
          rating: 4.8,
          price: '$119',
          image: 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=400',
          category: 'Programming'
        }
      ];
      setCourses(mockCourses);
      setEnrolledCourses([mockCourses[0], mockCourses[3]]); // Simulate enrolled courses
      setLoading(false);
    }, 1000);
  }, []);

  const filteredCourses = courses.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         course.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filter === 'all' || course.category === filter;
    return matchesSearch && matchesFilter;
  });

  const categories = ['all', 'Programming', 'Web Development', 'Data Science', 'Design', 'Business'];

  const stats = [
    {
      label: 'Enrolled Courses',
      value: enrolledCourses.length,
      icon: BookOpen,
      color: 'blue',
      change: '+2 this month'
    },
    {
      label: 'Hours Learned',
      value: '24.5',
      icon: Clock,
      color: 'green',
      change: '+8.2 this week'
    },
    {
      label: 'Certificates',
      value: '3',
      icon: Award,
      color: 'purple',
      change: '+1 this month'
    },
    {
      label: 'Learning Streak',
      value: '12 days',
      icon: TrendingUp,
      color: 'orange',
      change: 'Personal best!'
    }
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="header-brand">
            <BookOpen className="w-8 h-8 text-blue-600" />
            <span>EduLearn</span>
          </div>
          
          <div className="header-actions">
            <button className="header-button" title="Notifications">
              <Bell className="w-6 h-6" />
            </button>
            <div className="flex items-center gap-2">
              <div className="avatar">
                {user?.username?.charAt(0).toUpperCase()}
              </div>
              <span className="text-sm font-medium text-gray-700">{user?.username}</span>
            </div>
            <button
              onClick={logout}
              className="header-button"
              title="Logout"
            >
              <LogOut className="w-5 h-5" />
            </button>
          </div>
        </div>
      </header>

      <div className="container py-8">
        {/* Welcome Section */}
        <div className="welcome-section">
          <div className="welcome-content">
            <h1 className="welcome-title">
              Welcome back, {user?.username}! 👋
            </h1>
            <p className="welcome-subtitle">
              Continue your learning journey with our amazing courses
            </p>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => {
            const IconComponent = stat.icon;
            return (
              <div key={index} className="stats-card">
                <div className="stats-card-content">
                  <div className={`stats-icon ${stat.color}`}>
                    <IconComponent className="w-6 h-6" />
                  </div>
                  <div className="stats-info">
                    <div className="stats-label">{stat.label}</div>
                    <div className="stats-value">{stat.value}</div>
                    <div className="text-xs text-green-600 font-medium">{stat.change}</div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Search and Filter */}
        <div className="mb-8">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="search-container">
              <Search className="search-icon w-5 h-5" />
              <input
                type="text"
                placeholder="Search courses..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
            </div>
            <div className="flex items-center gap-2">
              <Filter className="w-5 h-5 text-gray-400" />
              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="select-input"
              >
                {categories.map(category => (
                  <option key={category} value={category}>
                    {category === 'all' ? 'All Categories' : category}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Enrolled Courses */}
        {enrolledCourses.length > 0 && (
          <div className="mb-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">My Courses</h2>
              <span className="badge badge-info">{enrolledCourses.length} Active</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {enrolledCourses.map(course => (
                <div key={course.id} className="course-card">
                  <img
                    src={course.image}
                    alt={course.title}
                    className="course-card-image"
                  />
                  <div className="course-card-content">
                    <div className="course-card-header">
                      <span className="course-category">{course.category}</span>
                      <div className="course-rating">
                        <Star className="w-4 h-4 fill-current" />
                        <span>{course.rating}</span>
                      </div>
                    </div>
                    <h3 className="course-title">{course.title}</h3>
                    <p className="course-description">{course.description}</p>
                    
                    {course.progress && (
                      <div className="mb-4">
                        <div className="flex justify-between text-sm text-gray-600 mb-1">
                          <span>Progress</span>
                          <span>{course.progress}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${course.progress}%` }}
                          ></div>
                        </div>
                      </div>
                    )}
                    
                    <div className="course-meta">
                      <span className="course-meta-item">
                        <Clock className="w-4 h-4" />
                        {course.duration}
                      </span>
                      <span className="course-meta-item">
                        <Users className="w-4 h-4" />
                        {course.students} students
                      </span>
                    </div>
                    <button className="btn btn-primary btn-full">
                      <Play className="w-4 h-4 mr-2" />
                      Continue Learning
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Available Courses */}
        <div>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Available Courses</h2>
            <span className="text-sm text-gray-600">{filteredCourses.length} courses found</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredCourses.map(course => (
              <div key={course.id} className="course-card">
                <img
                  src={course.image}
                  alt={course.title}
                  className="course-card-image"
                />
                <div className="course-card-content">
                  <div className="course-card-header">
                    <span className="course-category">{course.category}</span>
                    <div className="course-rating">
                      <Star className="w-4 h-4 fill-current" />
                      <span>{course.rating}</span>
                    </div>
                  </div>
                  <h3 className="course-title">{course.title}</h3>
                  <p className="course-description">{course.description}</p>
                  <div className="course-meta">
                    <span className="course-meta-item">
                      <Clock className="w-4 h-4" />
                      {course.duration}
                    </span>
                    <span className="course-meta-item">
                      <Users className="w-4 h-4" />
                      {course.students} students
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="course-price">{course.price}</span>
                    <button className="btn btn-secondary">
                      Enroll Now
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard; 