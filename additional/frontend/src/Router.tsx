import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom';
import { DemoPage } from '@/pages/Demo.page';
import { ResearchPage } from '@/pages/Research.page';

const router = createBrowserRouter([
    {
        path: '/',
        element: <Navigate to="/demo" replace />,
    },
    {
        path: '/demo',
        element: <DemoPage />,
    },
    {
        path: '/research',
        element: <ResearchPage />,
    }
]);

export function Router() {
    return <RouterProvider router={router} />;
}
