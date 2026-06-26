import { useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/auth'
import { getMe } from './api/auth'
import Layout from './components/Layout'
import Home from './pages/Home'
import PostDetail from './pages/PostDetail'
import CreatePost from './pages/CreatePost'
import Login from './pages/Login'
import Register from './pages/Register'
import Profile from './pages/Profile'
import Favorites from './pages/Favorites'
import ChatList from './pages/ChatList'
import ChatRoom from './pages/ChatRoom'
import UserPublicProfile from './pages/UserPublicProfile'

export default function App() {
  const { token, setUser, logout } = useAuthStore()

  useEffect(() => {
    if (token) {
      getMe().then(setUser).catch(() => logout())
    }
  }, [])

  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/posts/:id" element={<PostDetail />} />
          <Route path="/posts/create" element={<CreatePost />} />
          <Route path="/posts/:id/edit" element={<CreatePost />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/favorites" element={<Favorites />} />
          <Route path="/chat" element={<ChatList />} />
          <Route path="/chat/:id" element={<ChatRoom />} />
          <Route path="/users/:id" element={<UserPublicProfile />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}