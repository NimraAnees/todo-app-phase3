export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Welcome to Todo App</h1>
        <p className="text-gray-600 mb-8">
          A secure todo application with JWT authentication
        </p>
        <div className="space-x-4">
          <a
            href="/signup"
            className="inline-block bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition"
          >
            Sign Up
          </a>
          <a
            href="/signin"
            className="inline-block bg-gray-200 text-gray-800 px-6 py-3 rounded-md hover:bg-gray-300 transition"
          >
            Sign In
          </a>
        </div>
      </div>
    </main>
  );
}
