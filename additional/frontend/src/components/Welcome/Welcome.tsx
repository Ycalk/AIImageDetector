import { Anchor, Text, Title } from '@mantine/core';
import classes from './Welcome.module.css';

export function Welcome() {
    return (
        <>
            <Title className={classes.title} ta="center" mt={100}>
                AI Image{' '}
                <Text inherit variant="gradient" component="span" gradient={{ from: 'blue', to: 'cyan' }}>
                    Detector
                </Text>
            </Title>
            <Text c="dimmed" ta="center" size="lg" maw={580} mx="auto" mt="xl">
                Проект посвященный изучению возможности обнаружения сгенерированных с помощью
                нейросетей изображений. На вкладке "Исследование" можно подробней ознакомиться с
                ходом исследования и выбранной архитектурой. На этой вкладке можно протестировать
                работу модели.
            </Text>
        </>
    );
}
