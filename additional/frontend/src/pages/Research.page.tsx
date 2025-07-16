import { Header } from '@/components/Header/Header';
import ReactMarkdown from 'react-markdown';
import { useEffect, useState } from 'react';
import {
    Container,
    Loader,
    Table,
    Text,
    Image,
    Center,
    Blockquote,
    Title,
    TypographyStylesProvider
} from '@mantine/core';
import remarkGfm from 'remark-gfm';

export function ResearchPage() {
    const [markdown, setMarkdown] = useState<string | null>(null);

    useEffect(() => {
        fetch(
            'https://raw.githubusercontent.com/Ycalk/AIImageDetector/main/additional/research/README.md'
        )
            .then((res) => res.text())
            .then(setMarkdown)
            .catch((err) => {
                console.error('Failed to fetch markdown:', err);
                setMarkdown('# Ошибка загрузки отчета');
            });
    }, []);

    return (
        <>
            <Header />
            <Container size="md" py="xl">
                {markdown ? (
                    <TypographyStylesProvider>
                        <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            components={{
                                h1: ({ children }) => (
                                    <Title order={1} my="lg">
                                        {children}
                                    </Title>
                                ),
                                h2: ({ children }) => (
                                    <Title order={2} my="md">
                                        {children}
                                    </Title>
                                ),
                                h3: ({ children }) => (
                                    <Title order={3} my="sm">
                                        {children}
                                    </Title>
                                ),
                                p: ({ children }) => <Text my="md">{children}</Text>,
                                blockquote: ({ children }) => <Blockquote my="md">{children}</Blockquote>,
                                img: ({ src, alt }) => (
                                    <Center my="md">
                                        <Image radius="md" src={src || ''} alt={alt} fit="contain" w='auto' />
                                    </Center>
                                ),
                                table: ({ children }) => (
                                    <Table withTableBorder  >
                                        {children}
                                    </Table>
                                ),
                                thead: ({ children }) => (
                                    <Table.Thead>{children}</Table.Thead>
                                ),
                                tr: ({ children }) => <Table.Tr>{children}</Table.Tr>,
                                th: ({ children }) => <Table.Th>{children}</Table.Th>,
                                td: ({ children }) => <Table.Td>{children}</Table.Td>,
                            }}
                        >
                            {markdown}
                        </ReactMarkdown>
                    </TypographyStylesProvider>
                ) : (
                    <Center py="xl">
                        <Loader />
                    </Center>
                )}
            </Container>
        </>
    );
}
