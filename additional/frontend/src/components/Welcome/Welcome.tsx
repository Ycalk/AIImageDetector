import { Anchor, Text, Title } from '@mantine/core';
import classes from './Welcome.module.css';

export function Welcome() {
    return (
        <>
            <Title className={classes.title} ta="center" style={{
                fontSize: 'clamp(50px, 7vw, 90px)',
            }} >
                AI Image{' '}
                <Text inherit variant="gradient" component="span" gradient={{ from: 'blue', to: 'cyan' }}>
                    Detector
                </Text>
            </Title>
            <Text c="dimmed" ta="center" maw={580} mx="auto" style={{
                fontSize: 'clamp(15px, 1vw, 30px)',
            }}>
                Проект посвященный изучению возможности обнаружения сгенерированных с помощью
                нейросетей изображений. На вкладке "Исследование" можно подробней ознакомиться с
                ходом исследования и выбранной архитектурой. На этой вкладке можно протестировать
                работу модели.
            </Text>
        </>
    );
}
