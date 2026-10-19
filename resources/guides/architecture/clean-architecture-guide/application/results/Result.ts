// Plain output returned by use cases instead of throwing for business failures.
export class Result<T> {
  private constructor(
    private readonly ok: boolean,
    readonly value?: T,
    readonly error?: string
  ) {}

  static success<T>(value: T): Result<T> {
    return new Result<T>(true, value);
  }

  static failure<T>(error: string): Result<T> {
    return new Result<T>(false, undefined, error);
  }

  isSuccess(): boolean {
    return this.ok;
  }

  isFailure(): boolean {
    return !this.ok;
  }
}
