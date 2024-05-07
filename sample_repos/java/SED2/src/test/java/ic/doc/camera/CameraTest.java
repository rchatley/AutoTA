package ic.doc.camera;

import org.jmock.Expectations;
import org.jmock.integration.junit4.JUnitRuleMockery;
import org.junit.Rule;
import org.junit.Test;

public class CameraTest {

    @Rule
    public JUnitRuleMockery context = new JUnitRuleMockery();

    Sensor sensor = context.mock(Sensor.class);
    MemoryCard memoryCard = context.mock(MemoryCard.class);

    Camera camera = new Camera(sensor, memoryCard);

    @Test
    public void switchingTheCameraOnPowersUpTheSensor() {
        context.checking(new Expectations() {{
            exactly(1).of(sensor).powerUp();
        }});

        camera.powerOn();
    }

    @Test
    public void switchingTheCameraOffPowersDownTheSensor() {
        context.checking(new Expectations() {{
            exactly(1).of(sensor).powerDown();
        }});

        camera.powerOff();
    }

    @Test
    public void pressingTheShutterWhenThePowerIsOffDoesNothing() {
        context.checking(new Expectations() {{
            never(sensor).readData();
        }});

        camera.pressShutter();
    }

    @Test
    public void pressingTheShutterWhenThePowerIsOnCopiesData() {
        context.checking(new Expectations() {{
            byte[] data = new byte[]{};

            ignoring(sensor).powerUp();
            exactly(1).of(sensor).readData();
            will(returnValue(data));
            exactly(1).of(memoryCard).write(data);
        }});

        camera.powerOn();
        camera.pressShutter();
    }

    @Test
    public void switchingCameraOffDoesNotPowerDownSensorIfDataBeingWritten() {
        context.checking(new Expectations() {{
            ignoring(sensor).powerUp();
            ignoring(sensor).readData();
            ignoring(memoryCard).write(new byte[]{});
            never(sensor).powerDown();
        }});

        camera.powerOn();
        camera.pressShutter();
        camera.powerOff();
    }

    @Test
    public void oneWritingTheDataHasCompletedThenTheCameraPowersDownTheSensor() {
        context.checking(new Expectations() {{
            ignoring(sensor).powerUp();
            ignoring(sensor).readData();
            ignoring(memoryCard).write(new byte[]{});
            exactly(1).of(sensor).powerDown();
        }});

        camera.powerOn();
        camera.pressShutter();
        camera.writeComplete();
        camera.powerOff();
    }
}