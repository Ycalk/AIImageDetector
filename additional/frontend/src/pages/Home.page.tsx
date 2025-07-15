import { ColorSchemeToggle } from '../components/ColorSchemeToggle/ColorSchemeToggle';
import { Welcome } from '../components/Welcome/Welcome';
import { DropzoneButton } from '../components/DropzoneButton/DropzoneButton'
import { Container } from '@mantine/core';

export function HomePage() {
    return (
        <>
            <Welcome />
            <ColorSchemeToggle />
            <Container size="sm">
                <DropzoneButton />
            </Container>
        </>
    );
}
