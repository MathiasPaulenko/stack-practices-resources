// Plain input crossing the adapter -> application boundary.
export class RegisterUserCommand {
  constructor(readonly email: string) {}
}
