package main.example;

public class UpperROT13 extends Cryptosystem {

  @Override
  void transformInput() {
    this.text = this.text.toUpperCase();
  }

  @Override
  void applyCipher() {
    this.text = shiftString(13);
  }
}
