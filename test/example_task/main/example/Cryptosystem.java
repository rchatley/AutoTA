package main.example;

// Abstract class defining Template Method
abstract public class Cryptosystem {
  protected String text;

  // Template Method
  public String encryptString(String input) {
    text = input;
    transformInput();
    applyCipher();

    return text;
  }

  // Hook Method
  String shiftString(int shift) {
    shift = shift % 26;
    StringBuilder cipherText = new StringBuilder();

    for (char c : text.toCharArray()) {
      if (Character.isLetter(c)) {
        char base = Character.isLowerCase(c) ? 'a' : 'A';
        char shiftedChar = (char) ((c - base + shift + 26) % 26 + base);
        cipherText.append(shiftedChar);
      } else {
        cipherText.append(c);
      }
    }

    return cipherText.toString();
  }

  // Operations to be Implemented by Subclasses
  abstract void transformInput();
  abstract void applyCipher();
}
