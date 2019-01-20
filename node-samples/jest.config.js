export const testEnvironment = 'node';
export const transform = {
  "^.+\\.tsx?$": "ts-jest"
};
export const moduleFileExtensions = [
  "ts",
  "tsx",
  "js",
  "jsx",
  "json",
  "node",
];
export const testRegex = '(/__tests__/.*|(\\.|/)(test|spec))\\.(ts|js)x?$';
export const coverageDirectory = 'coverage';
export const collectCoverageFrom = [
  'src/**/*.{ts,tsx,js,jsx}',
  '!src/**/*.d.ts',
];
