import type { Repository } from "./repository.js";
import type { Model } from "mongoose";

/**
 * Mongoose-backed repository implementation.
 * Maps Mongoose documents to plain domain entities via toEntity().
 */
export class MongooseRepository<T extends { id: string }>
  implements Repository<T, string>
{
  constructor(private model: Model<any>) {}

  async findById(id: string): Promise<T | null> {
    const doc = await this.model.findById(id).lean();
    return doc ? this.toEntity(doc) : null;
  }

  async findAll(filter: Record<string, any> = {}): Promise<T[]> {
    const docs = await this.model.find(filter).lean();
    return docs.map((doc) => this.toEntity(doc));
  }

  async create(data: Omit<T, "id">): Promise<T> {
    const doc = await this.model.create(data);
    return this.toEntity(doc.toObject());
  }

  async update(id: string, data: Partial<T>): Promise<T | null> {
    const doc = await this.model
      .findByIdAndUpdate(id, data, { new: true })
      .lean();
    return doc ? this.toEntity(doc) : null;
  }

  async delete(id: string): Promise<boolean> {
    const result = await this.model.findByIdAndDelete(id);
    return !!result;
  }

  private toEntity(doc: any): T {
    const { _id, __v, ...rest } = doc;
    return { id: _id.toString(), ...rest } as T;
  }
}
