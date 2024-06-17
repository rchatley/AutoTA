package test.example;

import main.example.CaesarCipher;
import main.example.Cryptosystem;
import org.junit.Test;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.core.Is.is;

public class CaesarCipherTest {
  @Test
  public void testShiftZeroIsSelf() {
    Cryptosystem cryptosystem = new CaesarCipher(0);
    assertThat(cryptosystem.encryptString("Hello"), is("Hello"));
  }

  @Test
  public void testShiftOne() {
    Cryptosystem cryptosystem = new CaesarCipher(1);
    assertThat(cryptosystem.encryptString("Hello"), is("Ifmmp"));
  }
}