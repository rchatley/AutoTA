package main.example;


public class CaesarCipher extends Cryptosystem {
  final int cipherShift;

  public CaesarCipher(int shift) {
    this.cipherShift = shift;
  }

  // Intentionally missing @Override annotation for testing
  void transformInput() {
  }

  // Intentionally missing @Override annotation for testing
  void applyCipher() {
    this.text = shiftString(cipherShift);
  }
}
