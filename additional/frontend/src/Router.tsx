import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom';
import { DemoPage } from '@/pages/Demo.page';
import { ResearchPage } from '@/pages/Research.page';
import { NotFoundPage } from '@/pages/NotFound.page';

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
    },
    {
        path: '*',
        element: <NotFoundPage />,
    },
],
    {
        basename: '/AIImageDetector/',
    }
);

export function Router() {
    return <RouterProvider router={router} />;
}
