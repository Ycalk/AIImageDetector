import { Welcome } from '@/components/Welcome/Welcome';
import { DropzoneButton } from '@/components/DropzoneButton/DropzoneButton'
import { Space, Stack } from '@mantine/core';
import { Header } from '@/components/Header/Header';

export function DemoPage() {
    return (
        <>
            <Header />
            <Space h="xl"/>
            <Stack
                px="xl"
                bg="var(--mantine-color-body)"
                align="center"
                gap="xl"
            >
                <Welcome />
                <DropzoneButton />
            </Stack>
        </>
    );
}
