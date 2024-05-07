package ic.doc.camera;

public class Camera implements WriteListener {

    private Sensor sensor;
    private MemoryCard memoryCard;
    private boolean powerOn;
    private boolean writing;

    public Camera(Sensor sensor, MemoryCard memoryCard) {
        this.powerOn = false;
        this.sensor = sensor;
        this.memoryCard = memoryCard;
        this.writing = false;
    }

    public void pressShutter() {
        if (powerOn) {
            writing = true;
            memoryCard.write(sensor.readData());
        }
    }

    public void powerOn() {
        powerOn = true;
        sensor.powerUp();
    }

    public void powerOff() {
        if (!writing) {
            powerOn = false;
            sensor.powerDown();
        }
    }

    @Override
    public void writeComplete() {
        writing = false;
    }
}