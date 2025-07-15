import { useRef } from 'react';
import { IconCloudUpload, IconDownload, IconX } from '@tabler/icons-react';
import { Button, Group, Text, useMantineTheme } from '@mantine/core';
import { Dropzone, MIME_TYPES } from '@mantine/dropzone';
import classes from './DropzoneButton.module.css';

export function DropzoneButton() {
    const theme = useMantineTheme();
    const openRef = useRef<() => void>(null);

    return (
        <div className={classes.wrapper}>
            <Dropzone
                openRef={openRef}
                onDrop={() => { }}
                className={classes.dropzone}
                radius="md"
                accept={[MIME_TYPES.png, MIME_TYPES.jpeg]}
                maxSize={30 * 1024 ** 2}
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
                            <IconCloudUpload size={50} stroke={1.5} className={classes.icon} />
                        </Dropzone.Idle>
                    </Group>

                    <Text ta="center" fw={700} fz="lg" mt="xl" className={classes.infoText}>
                        <Dropzone.Accept>Отпустите здесь</Dropzone.Accept>
                        <Dropzone.Reject>Не изображение</Dropzone.Reject>
                        <Dropzone.Idle>Выбрать изображение</Dropzone.Idle>
                    </Text>

                    <Text className={classes.description}>
                        Перетащите файл с изображение или нажмите кнопку ниже, чтобы выбрать файл.
                    </Text>
                </div>
            </Dropzone>

            <Button className={classes.control} size="md" radius="xl" onClick={() => openRef.current?.()}>
                Выбрать файл
            </Button>
        </div>
    );
}