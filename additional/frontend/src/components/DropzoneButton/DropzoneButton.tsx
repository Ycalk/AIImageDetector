import { useRef, useState } from 'react';
import { IconCloudUpload, IconDownload, IconX } from '@tabler/icons-react';
import {
    Button,
    Group,
    Text,
    useMantineTheme,
    Loader,
    Notification,
} from '@mantine/core';
import { Dropzone, MIME_TYPES } from '@mantine/dropzone';
import { Space } from '@mantine/core';
import classes from './DropzoneButton.module.css';

export function DropzoneButton() {
    const theme = useMantineTheme();
    const openRef = useRef<() => void>(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<number | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleDrop = async (files: File[]) => {
        if (files.length === 0) return;

        const file = files[0];
        const formData = new FormData();
        formData.append('image', file);

        setLoading(true);
        setResult(null);
        setError(null);

        try {
            const response = await fetch('/api/detect', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText || 'Ошибка при загрузке');
            }

            const data = await response.json();
            setResult(data.result);
        } catch (err: any) {
            setError(err.message || 'Неизвестная ошибка');
        } finally {
            setLoading(false);
        }
    };

    const getNotificationColor = () => {
        if (result === null) return 'blue';
        if (result > 0.6) return 'orange';
        if (result > 0.4) return 'yellow';
        return 'green';
    };


    return (
        <div className={classes.wrapper}>
            {result !== null && (
                <div>
                    <Notification
                        color={getNotificationColor()}
                        mt="md"
                        withCloseButton
                        onClose={() => setResult(null)}
                    >
                        Результат: {(result * 100).toFixed(0)}% уверенности, что изображение сгенерировано ИИ
                    </Notification>
                    <Space h="sm" />
                </div>
            )}

            {error && (
                <div>
                    <Notification
                        color="red"
                        mt="md"
                        withCloseButton
                        onClose={() => setError(null)}
                    >
                        Ошибка: {error}
                    </Notification>
                    <Space h="sm" />
                </div>
            )}

            <Dropzone
                openRef={openRef}
                onDrop={handleDrop}
                className={classes.dropzone}
                radius="md"
                accept={[MIME_TYPES.png, MIME_TYPES.jpeg]}
                maxSize={30 * 1024 ** 2}
                disabled={loading}
            >
                <div style={{ pointerEvents: 'none' }}>
                    <Group justify="center">
                        <Dropzone.Accept>
                            <IconDownload size={50} color={theme.colors.blue[6]} stroke={1.5} />
                        </Dropzone.Accept>
                        <Dropzone.Reject>
                            <IconX size={50} color={theme.colors.red[6]} stroke={1.5} />
                        </Dropzone.Reject>
                        <Dropzone.Idle>
                            {loading ? (
                                <Loader size={50} />
                            ) : (
                                <IconCloudUpload size={50} stroke={1.5} className={classes.icon} />
                            )}
                        </Dropzone.Idle>
                    </Group>

                    <Text ta="center" fw={700} fz="lg" mt="xl" className={classes.infoText}>
                        <Dropzone.Accept>Отпустите здесь</Dropzone.Accept>
                        <Dropzone.Reject>Не изображение</Dropzone.Reject>
                        <Dropzone.Idle>
                            {loading ? 'Анализ изображения...' : 'Выбрать изображение'}
                        </Dropzone.Idle>
                    </Text>

                    <Text className={classes.description}>
                        Перетащите файл с изображением или нажмите кнопку ниже, чтобы выбрать файл.
                    </Text>
                </div>
            </Dropzone>

            <Button
                className={classes.control}
                size="md"
                radius="xl"
                onClick={() => openRef.current?.()}
                disabled={loading}
            >
                {loading ? <Loader size="xs" color="white" /> : 'Выбрать файл'}
            </Button>
        </div>
    );
}
