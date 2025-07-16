import { useLocation, Link } from 'react-router-dom';
import { Burger, Container, Group } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { ColorSchemeToggle } from '../ColorSchemeToggle/ColorSchemeToggle';
import classes from './HeaderSimple.module.css';

const links = [
    { link: '/demo', label: 'Демонстрация' },
    { link: '/research', label: 'Исследование' },
];

export function Header() {
    const location = useLocation(); // 🧠 Текущий путь

    const items = links.map((link) => (
        <Link
            key={link.label}
            to={link.link}
            className={classes.link}
            data-active={location.pathname === link.link || undefined}
        >
            {link.label}
        </Link>
    ));

    return (
        <header className={classes.header}>
            <Container size="md" className={classes.inner}>
                <Group gap={10}>
                    {items}
                </Group>
                <ColorSchemeToggle />
            </Container>
        </header>
    );
}
