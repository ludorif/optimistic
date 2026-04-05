import {describe, expect, test} from '@jest/globals';
import {isGreaterThan} from './Helper';

describe('isGreaterThan', () => {
  test('is 1 GreaterThan 2', () => {
    expect(isGreaterThan(1, 2)).toBe(false);
  });

  test('is 2 GreaterThan 1', () => {
    expect(isGreaterThan(2, 1)).toBe(true);
  });

  test('is C GreaterThan A', () => {
    expect(isGreaterThan("C", "A")).toBe(true);
  });
});