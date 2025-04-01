import React, { useState, useEffect } from 'react';
import '../styles/Exercises.css';

interface muscle_group {
  id:number;
  name: string;
}

interface equipment {
  id:number;
  name: string;
}

interface Exercise {
  id: string;  // UUID
  name: string;
  description: string;
  difficulty: string;
  muscle_groups: muscle_group[];  // Changed from muscleGroups to muscle_group
  equipment: equipment[];
}

interface ApiResponse {
  data: Exercise[];
  total: number;
  page: number;
  limit: number;
}

interface CacheEntry {
  data: ApiResponse;
  timestamp: number;
}

// Cache configuration
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes in milliseconds
const cache = new Map<string, CacheEntry>();

const getCacheKey = (params: URLSearchParams): string => {
  return params.toString();
};

const isCacheValid = (entry: CacheEntry): boolean => {
  return Date.now() - entry.timestamp < CACHE_DURATION;
};

// Mock categories data
const MOCK_CATEGORIES = [
  'Chest',
  'Back',
  'Shoulders',
  'Arms',
  'Core',
  'Legs',
];

const Exercises: React.FC = () => {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [debouncedSearchQuery, setDebouncedSearchQuery] = useState('');
  const [difficultyFilter, setDifficultyFilter] = useState<string>('');
  const [muscleGroupFilter, setMuscleGroupFilter] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [totalExercises, setTotalExercises] = useState(0);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  // Fetch categories on mount
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        console.log('Fetching categories...');
        const response = await fetch('/api/categories');
        console.log('Categories response status:', response.status);
        if (!response.ok) {
          throw new Error('Failed to fetch categories');
        }
        const data = await response.json();
        console.log('Categories data:', data);
        // If data is nested in a result property, extract it
        const categoriesList = data.result || data;
        setCategories(categoriesList);
      } catch (err) {
        console.log('Using mock categories data');
        setCategories(MOCK_CATEGORIES);
      }
    };

    fetchCategories();
  }, []);

  // Debounce search query
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearchQuery(searchQuery);
    }, 500);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  const fetchExercises = async (resetPage: boolean = false) => {
    try {
      setLoading(true);
      setError(null);
      
      const pageToFetch = resetPage ? 1 : page + 1;
      const params = new URLSearchParams();
      if (debouncedSearchQuery) params.append('search', debouncedSearchQuery);
      if (difficultyFilter) params.append('difficulty', difficultyFilter);
      if (muscleGroupFilter) params.append('category', muscleGroupFilter);
      params.append('limit', '12');
      params.append('page', pageToFetch.toString());

      const cacheKey = getCacheKey(params);
      const cachedEntry = cache.get(cacheKey);

      if (cachedEntry && isCacheValid(cachedEntry)) {
        console.log('Using cached data for:', cacheKey);
        const result = cachedEntry.data;
        
        if (resetPage) {
          setExercises(result.data);
          setPage(1);
        } else {
          setExercises(prev => [...prev, ...result.data]);
          setPage(pageToFetch);
        }
        
        setTotalExercises(result.total);
        setHasMore(result.data.length === 12);
        setLoading(false);
        return;
      }

      const response = await fetch(`/api/exercises?${params.toString()}`);
      if (!response.ok) {
        throw new Error('Failed to fetch exercises');
      }

      const result = await response.json();
      console.log('API Response:', result);

      if (!result.data || !Array.isArray(result.data)) {
        throw new Error('Invalid response format');
      }

      // Cache the response
      cache.set(cacheKey, {
        data: result,
        timestamp: Date.now()
      });

      if (resetPage) {
        setExercises(result.data);
        setPage(1);
      } else {
        setExercises(prev => [...prev, ...result.data]);
        setPage(pageToFetch);
      }
      
      setTotalExercises(result.total);
      setHasMore(result.data.length === 12);
    } catch (err) {
      console.error('Error fetching exercises:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch exercises');
    } finally {
      setLoading(false);
    }
  };

  // Clean up old cache entries periodically
  useEffect(() => {
    const cleanup = setInterval(() => {
      for (const [key, entry] of cache.entries()) {
        if (!isCacheValid(entry)) {
          cache.delete(key);
        }
      }
    }, 60000); // Check every minute

    return () => clearInterval(cleanup);
  }, []);

  // Reset page when filters change
  useEffect(() => {
    fetchExercises(true);
  }, [debouncedSearchQuery, difficultyFilter, muscleGroupFilter]);

  const handleLoadMore = () => {
    fetchExercises(false);
  };


  return (
    <div className="exercises-page">
      <div className="exercises-header">
        <h1>Exercise Library</h1>
        <p>Browse our collection of calisthenics exercises</p>
        <div className="header-actions">
          <div className="total-count">
            Showing {exercises.length} of {totalExercises} exercises
          </div>
          <a href="/docs" className="docs-link">
            API Documentation →
          </a>
        </div>
      </div>

      <div className="exercises-filters">
        <div className="search-box">
          <input
            type="text"
            className="search-input"
            placeholder="Search exercises..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <div className="filter-group">
          <select
            className="filter-select"
            value={difficultyFilter}
            onChange={(e) => setDifficultyFilter(e.target.value)}
          >
            <option value="">All Difficulties</option>
            <option value="beginner">Beginner</option>
            <option value="noivce">Novice</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
            <option value="elite">Elite</option>
          </select>

          <select
            className="filter-select"
            value={muscleGroupFilter}
            onChange={(e) => setMuscleGroupFilter(e.target.value)}
          >
            <option value="">All Categories</option>
            {categories && categories.length > 0 ? (
              categories.map(category => (
                <option key={category} value={category}>{category}</option>
              ))
            ) : (
              <option value="" disabled>Loading categories...</option>
            )}
          </select>
        </div>
      </div>

      {loading && <div className="loading">Loading exercises...</div>}
      {error && <div className="error">{error}</div>}
      
      <div className="exercises-grid">
        {exercises.map(exercise => (
          <div key={exercise.id} className="exercise-card">
            <span className={`difficulty-badge ${exercise.difficulty}`}>
              {exercise.difficulty.toUpperCase()}
            </span>
            <h3>{exercise.name}</h3>
            <p>{exercise.description}</p>
            <div className="exercise-tags">
              {/* <div className="muscle-groups">
                <span className="tag">{exercise.muscle_group}</span>
              </div> */}
              <div className="muscle-groups">
                {exercise.muscle_groups.map(item => (
                  <span key={item.id} className="tag">{item.name}</span>
                ))}
              </div>
              <div className="equipment">
                {exercise.equipment.map(item => (
                  <span key={item.id} className="tag equipment">{item.name}</span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      {hasMore && !loading && (
        <div className="load-more">
          <button 
            className="btn btn-outline" 
            onClick={handleLoadMore}
          >
            Load More Exercises
          </button>
        </div>
      )}
    </div>
  );
};


export default Exercises; 