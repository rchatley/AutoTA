package test.example;

import main.example.Cryptosystem;
import main.example.UpperROT13;
import org.junit.Test;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.core.Is.is;

public class UpperROT13Test {
  Cryptosystem cryptosystem = new UpperROT13();

  @Test
  public void encryptsUpperCase() {
    assertThat(cryptosystem.encryptString("HELLO"), is("URYYB"));
  }

  @Test
  public void encryptsLowerCase() {
    assertThat(cryptosystem.encryptString("hello"), is("URYYB"));
  }
}
